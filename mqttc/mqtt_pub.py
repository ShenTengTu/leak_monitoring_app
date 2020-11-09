# mosquitto MQTT publisher for testing
import sys
import subprocess
import shlex
import signal
from uuid import getnode
from pathlib import Path

path_here = Path(__file__).parent


def get_local_ip():
    return subprocess.getoutput("hostname -I | awk '{print $1}'")


class MQTT_Pub:
    def __init__(self, arg_dict: dict):
        _arg_dict = dict((k, shlex.quote(v)) for k, v in arg_dict.items())
        self.__cmd = " ".join(
            (
                "mosquitto_pub",
                *(e for item in _arg_dict.items() for e in item),
            )
        )
        self.__proc = None
        signal.signal(signal.SIGINT, self.__sig_int)

    def __sig_int(self, signal, frame):
        print("\nKeyboardInterrupt (ID: {})".format(signal))
        if self.__proc:
            self.__proc.kill()
        sys.exit(0)

    def __call__(self):
        self.__proc = subprocess.Popen(self.__cmd, shell=True)
        self.__proc.wait()


pub_topic = (
    lambda device, prop: "cgmh/nephrology/dialysis/leak_monitoring/{}/{}".format(
        device, prop
    )
)

CLIENT_ID = hex(getnode())[2:]
HOST = get_local_ip()
PORT = 1883
USER = "cgmh_leak_alert_0"
TOPIC = pub_topic(USER, "alert_level")
QOS = 1

pub_file = path_here / "pub_bin"


def mk_pub_file(data=b"\x14\xfb\x9c\x03\xd9\x7e"):
    with pub_file.open("wb") as fp:
        fp.write(data)


def main(binary_data: bytes):
    publish = MQTT_Pub(
        {
            "-i": CLIENT_ID,
            "-h": HOST,
            "-p": str(PORT),
            "-u": USER,
            # "-P": "",
            "-t": TOPIC,
            "-q": str(QOS),
            "-f": str(pub_file),
        },
    )

    mk_pub_file(binary_data)
    publish()


if __name__ == "__main__":
    from .bin_msg import get_message

    main(get_message())
