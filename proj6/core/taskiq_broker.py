__all__ = ("broker",)

from taskiq_aio_pika import AioPikaBroker
from .config import settings

broker = AioPikaBroker(
    url=str(settings.taskiq.url),
)
