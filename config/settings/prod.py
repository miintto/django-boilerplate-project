from .base import *


DEBUG = False

ALLOWED_HOSTS = ["*"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{message}",
            "style": "{"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "level": "INFO",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/api_service.log"),
            "when": "midnight",
            "formatter": "default",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "app_test": {
            "handlers": ["file", "console"],
            "level": "INFO",
            "propagate": True
        },
    }
}
