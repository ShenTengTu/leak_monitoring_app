import logging
from uvicorn.config import LOGGING_CONFIG, LOG_LEVELS

LOGGING_CONFIG["loggers"]["app_server"] = dict(handlers=["default"], level="INFO")


def set_log_level(level: str):
    log_level = LOG_LEVELS[level]
    logging.getLogger("app_server").setLevel(log_level)
