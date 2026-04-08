__all__ = ("broker",)

import logging

from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker

# import taskiq_fastapi
from .config import settings

log = logging.getLogger(__name__)

broker = AioPikaBroker(
    url=str(settings.taskiq.url),
)

# taskiq_fastapi.init(broker, "main:app")


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.taskiq.log_format,
    )
    log.info("Worker startup complete, state %s", state)
