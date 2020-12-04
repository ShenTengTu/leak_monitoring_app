import logging
import io
from asyncio import Queue
from sse_starlette.sse import (
    EventSourceResponse as _EventSourceResponse,
    AppStatus,
    ServerSentEvent,
)
from .endec import Encode

logger = logging.getLogger("app_server")


class EventSourceResponse(_EventSourceResponse):
    """Override original `EventSourceResponse`.

    If data is `None`, send comment to keep connections.
    """

    @staticmethod
    def comment_encode(content: str = "", sep: str = None) -> bytes:
        buffer = io.StringIO()
        buffer.write(f": {content}")
        buffer.write(sep if sep is not None else "\r\n")
        return buffer.getvalue().encode("utf-8")

    async def stream_response(self, send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.status_code,
                "headers": self.raw_headers,
            }
        )

        self._ping_task = self._loop.create_task(self._ping(send))  # type: ignore

        async for data in self.body_iterator:
            if AppStatus.should_exit:
                logger.debug(f"Caught signal. Stopping stream_response loop.")
                break
            if isinstance(data, dict):
                chunk = ServerSentEvent(**data).encode()
            elif data is None:
                chunk = self.comment_encode("NONE", sep=self.sep)
            else:
                chunk = ServerSentEvent(str(data), sep=self.sep).encode()
            logger.debug(f"[EventSourceResponse] chunk: {chunk.decode()}")
            await send({"type": "http.response.body", "body": chunk, "more_body": True})
        await send({"type": "http.response.body", "body": b"", "more_body": False})


class SSEManager:
    __queue = Queue()

    @classmethod
    def push_event(cls, event: str, data: dict):
        cls.__queue.put_nowait(dict(event=event, data=Encode.json(data)))

    @classmethod
    async def next_event(cls):
        q = cls.__queue
        if q.empty():
            return None
        item = await q.get()
        q.task_done()
        return item
