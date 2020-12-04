from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware


def middlewares():
    _middlewares = [Middleware(AuthenticationMiddleware)]
