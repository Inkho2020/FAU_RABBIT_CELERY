"""
- declare exchange for email....
- bind queue
- start consumer messaging
"""

import logging

from typing import TYPE_CHECKING, Callable
from pika.exchange_type import ExchangeType

from rabbit.base import RabbitBase
from rabbit import RMQ_config as Config

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import (
        Basic,
        BasicProperties,
    )

log = logging.getLogger(__name__)


class SimpleRabbitMixin:
    channel: "BlockingChannel"

    def declare_queue(self) -> None:
        self.channel.exchange_declare(
            exchange=Config.RMQ_DEAD_LETTER_EXCHANGE,
            exchange_type=ExchangeType.fanout,  # для fanout необходимо указать имя exchange без ключей
            # exchange_type=ExchangeType.topic,
        )
        dlq = self.channel.queue_declare(
            queue=Config.RMQ_DEAD_LETTER_KEY,
            durable=True,
        )
        self.channel.queue_bind(
            queue=dlq.method.queue,
            exchange=Config.RMQ_DEAD_LETTER_EXCHANGE,
            # routing_key=Config.RMQ_DEAD_LETTER_KEY,         # важно для topic
        )
        log.info("Created dlq: %s", dlq.method.queue)
        queue = self.channel.queue_declare(
            queue=Config.RMQ_ROUTING_KEY,
            durable=True,
            arguments={
                "x-dead-letter-exchange": Config.RMQ_DEAD_LETTER_EXCHANGE,
                # "x-dead-letter-routing-key": Config.RMQ_DEAD_LETTER_KEY,          # важно для topic
            },
        )
        log.info("Declare Queue: %s", queue.method.queue)

    def consume_messages(
        self,
        message_callback: Callable[
            [
                "BlockingChannel",
                "Basic.Deliver",
                "BasicProperties",
                bytes,
            ],
            None,
        ],
        prefetch_count: int = 1,
    ):
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.declare_queue()
        self.channel.basic_consume(
            queue=Config.RMQ_ROUTING_KEY,
            on_message_callback=message_callback,
            # auto_ack = True,
        )
        log.warning("Waiting for messages")
        self.channel.start_consuming()


class SimpleRabbit(SimpleRabbitMixin, RabbitBase):
    pass
