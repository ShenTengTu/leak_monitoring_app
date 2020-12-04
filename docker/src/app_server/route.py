from starlette.routing import Route, Mount
from .endpoint import EMQXWebHook, SSE
from .sse import SSEManager
from .conf import static_files


async def source_fn(parameter_list):
    pass


def routes():
    _routes = [
        Mount(
            "/api",
            name="api",
            routes=[Route("/emqx/web_hook", EMQXWebHook, name="emqx_web_hook")],
        ),
        Mount(
            "/sse",
            name="sse",
            routes=[
                Route(
                    "/alert_devices",
                    SSE(SSEManager.next_event).endpoint,
                    name="alert_devices",
                )
            ],
        ),
        Mount("/static", name="static", app=static_files),
    ]

    return _routes
