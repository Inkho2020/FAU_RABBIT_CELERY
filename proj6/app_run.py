import logging
from typing import AsyncGenerator

from core import (
    settings,
    db_session,
    broker,
)
from fastapi import FastAPI

logging.basicConfig(
    level=settings.logging.log_level_value,
    format=settings.logging.log_format,
)
log = logging.INFO


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    await broker.startup()
    yield
    # shutdown
    await db_session.dispose()
    await broker.shutdown()


def run():
    app = FastAPI(
        prefix=settings.api.prefix,
        lifespan=lifespan,
    )
    return app
