import logging
from .data_class import DC_EMQXWebHookBody, DCSet_EMQXWebHookBody
from .endec import Decode
from .sse import SSEManager

logger = logging.getLogger("app_server")


class Tasks:
    @staticmethod
    async def emqx_webhook_to_sse(data_ins: DC_EMQXWebHookBody):
        event = "mqtt_{}".format(data_ins.action)
        SSEManager.push_event(event, data_ins.as_dict())

    @staticmethod
    async def emqx_webhook_process_message(
        data_ins: DCSet_EMQXWebHookBody.message_publish,
    ):
        payload = Decode.base64(data_ins.payload)
        if payload is None:
            logging.warning("[EMQX web hook] Base64 decoding failed.")
            return
        payload = Decode.x_msgpack(payload)
        event = "mqtt_{}".format(data_ins.action)
        data = data_ins.as_dict()
        data["payload"] = payload
        SSEManager.push_event(event, data)
