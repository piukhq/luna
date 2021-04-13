import logging
import os
import sys

from logging.config import dictConfig
from typing import Any, Callable, Union

from dotenv import load_dotenv

from app.cache import LocalCache, RedisCache


def get_env(key: str, default: Any = None, *, conv: Callable = str) -> Any:
    val = os.getenv(key, default)
    if val is None:
        raise KeyError("Missing required variable %s" % key)  # pragma: no cover
    else:
        return conv(val)


def to_bool(val: Union[str, bool]) -> bool:
    if isinstance(val, bool):
        return val

    val = val.lower()
    if val not in ["true", "false"]:
        raise KeyError("'%s' is not an acceptable value for a bool" % val)

    return val == "true"


load_dotenv()

DEBUG = get_env("DEBUG", False, conv=to_bool)
LUNA_PORT = get_env("LUNA_PORT", 9000, conv=int)
LOG_FORMATTER = get_env("LOG_FORMATTER", "json")
ROOT_LOG_LEVEL = get_env("ROOT_LOG_LEVEL", "INFO")
DEFAULT_TIMEOUT_WAIT = get_env("ROOT_LOG_LEVEL", 150, conv=int)
DEFAULT_FAILED_RESPONSES = get_env("DEFAULT_FAILED_RESPONSES", 3, conv=int)
URL_PREFIX = get_env("URL_PREFIX", "")
USE_REDIS_CACHE = get_env("USE_REDIS_CACHE", False, conv=to_bool)

cache: Union[RedisCache, LocalCache]

if USE_REDIS_CACHE:
    REDIS_URL = get_env("REDIS_URL")  # pragma: no cover
    cache = RedisCache(REDIS_URL)  # pragma: no cover
else:
    cache = LocalCache()

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "gunicorn_style": {
                "format": "[%(asctime)s] [%(process)s] [%(levelname)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z",
            },
            "brief": {"format": "%(levelname)s:     %(asctime)s - %(message)s"},
            "json": {"()": "app.reporting.JSONFormatter"},
        },
        "handlers": {
            "stderr": {
                "level": logging.NOTSET,
                "class": "logging.StreamHandler",
                "stream": sys.stderr,
                "formatter": LOG_FORMATTER,
            },
            "stdout": {
                "level": logging.NOTSET,
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": LOG_FORMATTER,
            },
        },
        "loggers": {
            "root": {
                "level": ROOT_LOG_LEVEL or logging.INFO,
                "handlers": ["stdout"],
            },
        },
    }
)
