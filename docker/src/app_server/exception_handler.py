import logging
from http import HTTPStatus
from starlette.requests import Request
from starlette.exceptions import HTTPException
from .conf import TemplateResponse

logger = logging.getLogger("app_server")

_http_error_status = tuple(e for e in HTTPStatus if e.value >= 400)


class _ExceptionHandlers:
    __handlers = {}

    @classmethod
    async def http_error_handler(cls, request: Request, exc: HTTPException):
        context = dict(request=request, http_status=HTTPStatus(exc.status_code))
        return TemplateResponse("http_error.jinja", context)

    @classmethod
    def init(cls):
        for e in _http_error_status:
            cls.__handlers[e.value] = cls.http_error_handler
        return cls.__handlers.copy()


def exception_handlers():
    return _ExceptionHandlers.init()
