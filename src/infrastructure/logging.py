import logging

from src.config import settings


def configure_logging(log_level: str | int = settings.LOG_LEVEL):
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )
