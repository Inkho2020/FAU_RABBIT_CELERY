import logging
from datetime import datetime
import random
from time import time, sleep

from rabbit.RMQ_config import (
    config_logging,
)

from rabbit.Exchanges import PaintRabbit


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


def process_paint_button(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("channel: %s", channel)
    log.info("method: %s", method)
    log.info("properties: %s", properties)
    log.info("body: %s", body)

    log.warning("Start painting button %r", body)
    sleep(0.3)
    if random.random() < 0.2:
        log.warning("Solved task painting %r", body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return  # НЕ МОЖЕМ повторно подтвердить одно и тоже сообщение ????
    else:
        log.warning("Painting task failed %r,", body)
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    log.warning("Finished processing of painting %r", body)


def main():
    config_logging(level=logging.WARNING)
    with PaintRabbit() as broker:
        broker.consume_messages(
            message_callback=process_paint_button,
        )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
