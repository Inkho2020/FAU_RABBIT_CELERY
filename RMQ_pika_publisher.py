import logging
from datetime import datetime
from time import time

from RMQ_pika_config import (
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


def produce_message(channel: "BlockingChannel") -> None:
    queue = channel.queue_declare(
        queue=RMQ_ROUTING_KEY,
        durable=True,
    )
    log.info("Declare Queue %s %s", RMQ_ROUTING_KEY, queue)
    message_body = f"Hello World {record_time}"
    log.info("Published message %s", message_body)
    channel.basic_publish(
        exchange=RMQ_EXCHANGE,
        routing_key=RMQ_ROUTING_KEY,
        body=message_body,
    )


def main():
    config_logging()
    with get_connection() as connection:
        log.info("Starting connection %s", connection)
        with connection.channel() as channel:
            log.info("Open channel %s", channel)
            produce_message(channel=channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
