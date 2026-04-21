import logging
from typing import Any


LOGGER_NAME = "brand-engine"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_sanity(message: str, **extra: Any) -> None:
    get_logger().warning("%s %s", message, extra if extra else "")
