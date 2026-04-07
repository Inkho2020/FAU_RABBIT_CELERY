import logging
from datetime import datetime
from time import time, sleep

from RMQ_pika_config import (
    config_logging,
)

from rabbit.common import WeatherRabbit


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


def process_new_weather(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("channel: %s", channel)
    log.info("method: %s", method)
    log.info("properties: %s", properties)
    log.info("body: %s", body)

    log.warning("Start reporting weather %r", body)
    sleep(6)
    log.warning("Finished reporting weather %r", body)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    config_logging(level=logging.WARNING)
    with WeatherRabbit() as broker:
        broker.consume_messages(
            message_callback=process_new_weather,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
