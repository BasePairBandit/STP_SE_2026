import os

# Where to store the log file (user home directory)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs","seqkitstp.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "standard": {
            "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,
            "formatter": "standard",
        },
    },

    "loggers": {
        "SeqKitSTP": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False,
        }
    },

    "root": {
        "level": "DEBUG",
        "handlers": ["console", "file"],
    },
}