import logging
import logging.config


def read_aoc_day_data_file(day: int) -> str:
    """Read the data file for ``day`` in AoC 2022."""
    with open(f"./data/day_{day:02}.txt", encoding="utf-8") as file:
        return file.read()


def configure_logger() -> None:
    """
    Configure logger.

    The default ("root") logger is set to be at level DEBUG, the main logger is set
    to be at level WARNING.

    NOTE: If you are making a library, you will want to ONLY use NullHandler.
    See: https://docs.python.org/3.7/howto/logging.html#library-config

    For more information on the ``log_config`` used here, see:
    https://stackoverflow.com/a/7507842
    """
    log_config = {
        "version": 1,
        "disable_existing_loggers": True,
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
        },
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": "WARNING",
                "propagate": False,
            },  # root
            "__main__": {  # used when __name__ == "__main__", ie, run as a module.
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(log_config)
