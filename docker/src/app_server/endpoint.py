import logging
from typing import Any, Callable, Coroutine, Union
from asyncio import sleep, CancelledError
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
from starlette.background import BackgroundTask
from .sse import EventSourceResponse
from .data_class import DC_EMQXWebHookBody, DCSet_EMQXWebHookBody
from .bg_task import Tasks

logger = logging.getLogger("app_server")


class EMQXWebHook(HTTPEndpoint):
    @staticmethod
    def _validate(data: dict):
        if "action" not in data:
            return
        action = data["action"]
        if not hasattr(DCSet_EMQXWebHookBody, action):
            return
        _data_class = getattr(DCSet_EMQXWebHookBody, action)
        try:
            data_ins = _data_class(**data)
            return data_ins
        except TypeError:
            return

    @staticmethod
    def _background_task(data_ins: DC_EMQXWebHookBody):
        action = data_ins.action
        if action in ("client_connected", "client_disconnected"):
            return BackgroundTask(Tasks.emqx_webhook_to_sse, data_ins)
        elif action == "message_publish":
            return BackgroundTask(Tasks.emqx_webhook_process_message, data_ins)

    async def post(self, request: Request):
        data = await request.json()
        data_ins = self._validate(data)
        if data_ins is None:
            return JSONResponse(data)
        return JSONResponse(data, background=self._background_task(data_ins))


class SSE:
    @staticmethod
    async def sse_source(
        request: Request,
        source_async_fn: Callable[[], Coroutine[Any, Any, Union[dict, None]]],
        period: float = 0.1,  # Do not too short
    ):
        i = 0
        try:
            while True:
                disconnected = await request.is_disconnected()
                if disconnected:
                    logger.info(f"[SSE] Disconnecting: {request.client}")
                    break
                d = await source_async_fn()
                if type(d) is dict:
                    d["id"] = i
                    yield d
                    i = (i + 1) % 2 ** 14
                else:
                    yield d
                await sleep(period)
            logger.info(f"[SSE] Disconnected: {request.client}")
        except CancelledError:
            logger.info(f"[SSE] Disconnected (via refresh/close): {request.client}")

    def __init__(self, source_async_fn: Callable[[], Coroutine[Any, Any, dict]]):
        self.source_async_fn = source_async_fn

    async def endpoint(self, request: Request):
        return EventSourceResponse(self.sse_source(request, self.source_async_fn))
