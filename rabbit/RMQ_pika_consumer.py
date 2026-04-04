import logging
import random
from datetime import datetime
from time import time

from pika.spec import (
    Basic,
    BasicProperties,
)

from RMQ_pika_config import (
    config_logging,
    # RMQ_EXCHANGE,
    RMQ_ROUTING_KEY,
)

from base import RabbitBase


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
    log.warning("Start processing message %r", body)
    # проверка доставки сообщения, auto_act может закрыть task без подтверждения
    # если есть подтверждение, то auto_act дергает пустое сообщение

    # Обработка сообщений через nack/reject и ack
    if random.random() > 0.7:
        log.info("---Process finished message %r, sending nack!", body)
        channel.basic_nack(delivery_tag=method.delivery_tag)
        # log.info("---Process finished message %r, sending nack(NO REQUEUE)!", body)
        # channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        # log.info("---Process finished message %r, sending REJECT!", body)
        # channel.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
    else:
        log.info("+++ Process finished message %r, sending ack!", body)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    log.warning("Finished processing message %r", body)


def consumer_message(channel: "BlockingChannel") -> None:
    # basic_qos(prefetch_counts)кол-во потребления задач за 1 раз, влияет на загруженность,
    # если запускать несколько консьюмеров одновременно, auto_ack должен быть False, basic.ack = True
    # auto_ack распределяет кол-во task, basic.act распределяет загруженность
    channel.basic_qos(prefetch_count=1)
    channel.queue_declare(
        RMQ_ROUTING_KEY,
        durable=True,
    )
    channel.basic_consume(
        queue=RMQ_ROUTING_KEY,
        on_message_callback=process_new_message,
        # auto_ack=True,
        # auto_ack отдает все задачи из очереди первому consumer,
        # либо при полной очереди распределяет задачи по количеству(round robin), а не по нагрузке
    )
    log.warning("Waiting for messages")
    channel.start_consuming()


def main():
    config_logging(level=logging.INFO)
    with RabbitBase() as broker:
        log.info("Starting connection %s", broker)
        log.info("Open channel %s", broker.channel)
        consumer_message(channel=broker.channel)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
