import logging
import random
from datetime import datetime
from time import time

from RMQ_pika_config import (
    config_logging,
)

from rabbit.common import SimpleRabbit


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


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
    log.warning("Start processing message %r", body)
    if random.random() > 0.5:
        # log.info("---Process finished message %r, sending nack!", body)
        # channel.basic_nack(delivery_tag=method.delivery_tag)
        log.info("---Process finished message %r, sending nack(NO REQUEUE)!", body)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        # log.info("---Process finished message %r, sending REJECT!", body)
        # channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
    else:
        log.info("+++ Process finished message %r, sending ack!", body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    log.warning("Finished processing message %r", body)


def main():
    config_logging(level=logging.INFO)
    with SimpleRabbit() as broker:
        broker.consume_messages(
            message_callback=process_new_message,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
