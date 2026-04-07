import logging
from datetime import datetime
from time import time

from rabbit.RMQ_config import (
    config_logging,
    get_connection,
    RMQ_EXCHANGE,
    RMQ_ROUTING_KEY,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


def declare_queue(
    channel: "BlockingChannel",
) -> None:
    queue = channel.queue_declare(
        queue=RMQ_ROUTING_KEY,
        durable=True,
    )
    log.info("Declare Queue %s %s", RMQ_ROUTING_KEY, queue)


def produce_message(channel: "BlockingChannel", idx: int) -> None:

    message_body = f"New message No. {idx:02d}"
    channel.basic_publish(
        exchange=RMQ_EXCHANGE,
        routing_key=RMQ_ROUTING_KEY,
        body=message_body,
    )
    log.warning("Published message %s", message_body)


def main():
    config_logging()
    with get_connection() as connection:
        log.info("Starting connection %s", connection)
        with connection.channel() as channel:
            log.info("Open channel %s", channel)
            declare_queue(channel=channel)
            for idx in range(1, 4):
                produce_message(channel=channel, idx=idx)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
