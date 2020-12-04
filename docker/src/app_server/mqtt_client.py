import os
import sys
import threading
import asyncio
import logging
import logging.config
from signal import signal, SIGINT, SIGTERM
from uvicorn.subprocess import spawn
from uvicorn.loops.uvloop import uvloop_setup
from gmqtt import Client as MQTTC
from gmqtt.mqtt.constants import MQTTv311
from gmqtt.mqtt.handler import MQTTConnectError
from .logging import LOGGING_CONFIG

logger = logging.getLogger("app_server.mqtt_client")


class MQTTConfig:
    def __init__(
        self,
        host="test.mosquitto.org",
        port=1883,
        ssl=False,
        keepalive=60,
        version=MQTTv311,
        reconnect_retries=-1,
        reconnect_delay=10,
    ):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.keepalive = keepalive
        self.version = version
        self.reconnect_retries = reconnect_retries
        self.reconnect_delay = reconnect_delay


class MQTTClient:
    def __init__(self, config: MQTTConfig):
        self.config = config
        self.client = None
        self.connected = False
        self.should_exit = False
        self.force_exit = False

    def _handle_exit(self, sig, frame):
        if self.should_exit:
            self.force_exit = True
        else:
            self.should_exit = True

    def _on_connect(self, client: MQTTC, flags, rc, properties):
        self.connected = True
        logger.info("Connected to MQTT broker.")

    def _on_disconnect(self, client, packet, exc=None):
        self.connected = False
        logger.info("Disconnected to MQTT broker.")

    def _on_subscribe(self, client, mid, qos, properties):
        pass

    def _on_unsubscribe(self, client, mid, qos):
        pass

    async def _on_message(self, client, topic, payload, qos, properties):
        pass
        return 0  # must return valid PUBACK code

    def run(self):
        ## In subprocess ##
        uvloop_setup()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.serve())

    async def serve(self):
        ## In subprocess ##
        process_id = os.getpid()
        loop = asyncio.get_event_loop()
        loop.add_signal_handler(SIGINT, self._handle_exit, SIGINT, None)
        loop.add_signal_handler(SIGTERM, self._handle_exit, SIGTERM, None)

        logger.info("Started MQTT client process [%d]", process_id)

        await self.startup()
        if self.should_exit:
            return
        await self.main_loop()
        await self.shutdown()

    async def startup(self):
        conf = self.config
        client = MQTTC("client-id")
        client.set_config(
            dict(
                reconnect_retries=conf.reconnect_retries,
                reconnect_delay=conf.reconnect_delay,
            )
        )
        client.on_connect = self._on_connect
        client.on_message = self._on_message
        client.on_disconnect = self._on_disconnect
        client.on_subscribe = self._on_subscribe
        client.on_unsubscribe = self._on_unsubscribe

        try:
            await client.connect(
                conf.host, conf.port, conf.ssl, conf.keepalive, conf.version
            )
        except MQTTConnectError as error:
            print(error)
        self.client = client

    async def main_loop(self):
        counter = 0
        should_exit = await self.on_tick(counter)
        while not should_exit:
            counter += 1
            counter = counter % 864000
            await asyncio.sleep(0.1)
            should_exit = await self.on_tick(counter)

    async def on_tick(self, counter):
        if self.should_exit:
            return True
        return False

    async def shutdown(self):
        if self.client:
            await self.client.disconnect()


class MQTTClientProcess:
    @staticmethod
    def main(client_run, stdin_fileno):
        ## In subprocess ##
        if stdin_fileno is not None:
            sys.stdin = os.fdopen(stdin_fileno)
        logging.config.dictConfig(LOGGING_CONFIG)
        client_run()  # MQTTClient.run()

    def __init__(self, client_run):
        self.client_run = client_run  # MQTTClient.run()
        self.process = None
        self.should_exit = threading.Event()
        self.pid = os.getpid()

    def _signal_handler(self, sig, frame):
        self.should_exit.set()

    def run(self):
        self.startup()
        self.should_exit.wait()
        self.shutdown()

    def startup(self):
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

        try:
            stdin_fileno = sys.stdin.fileno()
        except OSError:
            stdin_fileno = None

        process = spawn.Process(
            target=self.main,
            kwargs=dict(
                client_run=self.client_run,
                stdin_fileno=stdin_fileno,
            ),
        )
        process.start()
        self.process = process

    def shutdown(self):
        self.process.join()


def run(**kwargs):
    logging.config.dictConfig(LOGGING_CONFIG)
    config = MQTTConfig(**kwargs)
    client = MQTTClient(config)
    supervisor = MQTTClientProcess(client.run)
    supervisor.run()


if __name__ == "__main__":
    run()
