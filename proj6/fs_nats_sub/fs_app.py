import logging
import asyncio

# import uvicorn
from faststream import FastStream

from core import settings
from core.nats_broker import fs_broker as broker
from fs_nats_sub.users import router as nats_router

fs_app = FastStream(
    broker,
)

broker.include_router(nats_router)

# publisher = broker.publisher("")


@fs_app.after_startup
async def configure_logging():
    logging.basicConfig(
        level=settings.logging.log_level_value,
        format=settings.logging.log_format,
        datefmt=settings.logging.date_format,
    )


async def main():
    await fs_app.run()  # blocking method


if __name__ == "__main__":
    asyncio.run(main())
