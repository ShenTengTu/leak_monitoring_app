from importlib import reload
from uvicorn import run as uvicorn_run
from .conf import UVICORN_CONFIG


def main():
    # Use import string for reloading & workers
    uvicorn_run("app_server:app", **UVICORN_CONFIG)


if __name__ == "__main__":
    main()
