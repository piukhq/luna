import logging
import os
import sys

from logging.config import dictConfig

from dotenv import load_dotenv

load_dotenv()

LOG_FORMATTER = os.getenv("LOG_FORMATTER", "json")
ROOT_LOG_LEVEL = os.getenv("ROOT_LOG_LEVEL", "INFO")
DEFAULT_TIMEOUT_WAIT = int(os.getenv("ROOT_LOG_LEVEL", "150"))
DEFAULT_FAILED_RESPONSES = int(os.getenv("DEFAULT_FAILED_RESPONSES", "3"))

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
