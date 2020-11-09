import logging
from starlette.applications import Starlette
from starlette.responses import RedirectResponse
from .conf import DEBUG, TemplateResponse
from .route import routes
from .middleware import middlewares
from .exception_handler import exception_handlers
from .logging import set_log_level

logger = logging.getLogger("app_server")


def get_app():
    def on_startup():
        if DEBUG:
            set_log_level("debug")

    _app = Starlette(
        debug=DEBUG,
        routes=routes(),
        middleware=middlewares(),
        exception_handlers=exception_handlers(),
        on_startup=[on_startup],
    )

    @_app.route("/")
    async def homepage(request):
        return RedirectResponse("dashboard")

    @_app.route("/dashboard", name="dashboard")
    async def dashboard(request):
        context = dict(
            alert_device_prefix="cgmh_leak_alert",
            n_of_alert_device=4,
            members_of_each_device=4,
        )
        context.update(request=request)
        return TemplateResponse("dashboard.jinja", context)

    return _app
