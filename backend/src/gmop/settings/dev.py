import logging.config
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS += ["drf_yasg"]  # NOQA

CORS_ORIGIN_ALLOW_ALL = True

TIME_ZONE = "UTC"

LOGGING_CONFIG = None
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] %(message)s",
            "datefmt": "%m/%d/%Y %H:%M:%S",
        },
        "cid_verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(pathname)s:%(lineno)s] [cid: %(cid)s] %(message)s",
            "datefmt": "%m/%d/%Y %H:%M:%S",
        },
        "audit_trail": {
            "format": "%(asctime)s : %(message)s",
            "datefmt": "%m/%d/%Y %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "filters": {"correlation": {"()": "cid.log.CidContextFilter"},},
    "loggers": {
        "django": {"handlers": ["console"], "propagate": True, "level": "WARNING",},
        "project": {
            "handlers": ["console"],
            "level": "DEBUG",
            "filters": ["correlation"],
        },
        "audit_trail": {"handlers": ["console"], "level": "INFO"},
    },
}

logging.config.dictConfig(LOGGING)
