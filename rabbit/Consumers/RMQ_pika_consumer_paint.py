import logging
from datetime import datetime
import random
from time import time, sleep

from rabbit.RMQ_config import (
    config_logging,
    RMQ_EXCHANGE,
    RMQ_QUEUE_NOT_SOLVE_TASKS,
)

from rabbit.Exchanges import PaintRabbit


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


def extract_death_count(headers: dict[str, int]) -> int:
    if headers and headers.get("x-death"):
        for props in headers["x-death"]:
            if "count" in props:
                return int(props["count"])
    return 0


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
    death_count = extract_death_count(properties.headers)
    log.warning("Start painting button %r", body)
    sleep(0.1)
    if random.random() < 0.2:
        log.warning(
            "[\u2705]Solved task painting %r, after retries %d",
            body,
            death_count,
        )
        channel.basic_ack(delivery_tag=method.delivery_tag)
        return  # НЕ МОЖЕМ повторно подтвердить одно и тоже сообщение ????
    if death_count < 5:
        log.warning(
            "[\u274c]Painting task failed %r, retried %d",
            body,
            death_count,
        )
        channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return
    # log.warning(
    #     "[\u2620]Get rid of task %r after retries %d",
    #     body,
    #     death_count,
    # )
    # channel.basic_ack(delivery_tag=method.delivery_tag)
    log.warning(
        "Delay task %r after retries %d for retro",
        body,
        death_count,
    )
    channel.basic_publish(
        exchange=RMQ_EXCHANGE,
        routing_key=RMQ_QUEUE_NOT_SOLVE_TASKS,
        body=body,
        properties=properties,
    )
    channel.basic_ack(delivery_tag=method.delivery_tag)


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
