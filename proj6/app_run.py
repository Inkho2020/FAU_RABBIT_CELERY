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
    if not broker.is_worker_process:
        await broker.startup()
    yield
    # shutdown
    if not broker.is_worker_process:
        await db_session.dispose()
    await broker.shutdown()


def run():
    return FastAPI(
        lifespan=lifespan,
    )
