import logging
from core.config import settings
from fastapi import FastAPI

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)
log = logging.INFO


def run():
    app = FastAPI()
    return app


if __name__ == "__main__":
    run()
