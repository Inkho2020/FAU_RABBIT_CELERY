import logging
from datetime import datetime
from time import time, sleep

from pika.spec import (
    Basic,
    BasicProperties,
)

from rabbit.RMQ_config import (
    config_logging,
    RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES,
)

from rabbit.Exchanges import EmailUpdatesRabbit


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


def process_new_message(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("channel: %s", channel)
    log.info("method: %s", method)
    log.info("properties: %s", properties)
    log.info("body: %s", body)
    log.warning("Update user email for newsletters %r", body)
    start_time = time()
    sleep(3)
    end = time()
    log.info("GET SOME LETTER")
    channel.basic_ack(delivery_tag=method.delivery_tag)
    log.warning("Updated user email %r", body)


def main():
    config_logging(level=logging.INFO)
    with EmailUpdatesRabbit() as broker:
        broker.consume_messages(
            message_callback=process_new_message,
            queue_name=RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES,  # присваивание имени очереди
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
