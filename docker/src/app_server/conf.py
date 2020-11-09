from os import getenv as _getenv
from pathlib import Path as _Path
from starlette.config import Config
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
from .logging import LOGGING_CONFIG


def _import_config(path: _Path):
    if path.is_file():
        return Config(path)
    else:
        return Config(None)  # only os.environ


# Define in Dokerfile
APP_PROJECT = _getenv("APP_PROJECT", "ndlm_leak_monitoring_app")

PATH_LOCAL = _Path.home() / ".local"
PATH_CONFIG = PATH_LOCAL / "etc" / APP_PROJECT

_config = _import_config(PATH_CONFIG / ".env")
DEBUG = _config("DEBUG", cast=bool, default=False)

_path_here = _Path(__file__).parent
_templates = Jinja2Templates(directory=str(_path_here.parent / "templates"))

TemplateResponse = _templates.TemplateResponse
static_files = StaticFiles(directory=_path_here.parent / "static", check_dir=True)

UVICORN_CONFIG = dict(host="0.0.0.0", port=8000, log_config=LOGGING_CONFIG)
if DEBUG:
    UVICORN_CONFIG.update(
        debug=True, reload=True, reload_dirs=[str(_path_here.parent.parent.absolute())]
    )
