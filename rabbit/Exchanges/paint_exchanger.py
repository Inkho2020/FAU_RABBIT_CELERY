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


class PaintRabbitMixin:
    channel: "BlockingChannel"

    def publish_message(
        self,
        text: str,
        exchange: str = Config.RMQ_EXCHANGE_PAINT_BUTTON,
        routing_key: str = Config.RMQ_QUEUE_PAINT_BUTTON,
    ) -> None:

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=text,
        )
        log.info("Published message %s", text)

    def declare_nsq(self) -> str:
        nsq = self.channel.queue_declare(
            queue=Config.RMQ_QUEUE_NOT_SOLVE_TASKS,
            durable=True,
        )
        log.info("Declare nsq: %s", nsq.method.queue)
        return nsq.method.queue

    def declare_dlq(self) -> str:
        self.channel.exchange_declare(
            exchange=Config.RMQ_DLX_FAILED_PAINT_BUTTON,
            exchange_type=ExchangeType.fanout,  # для fanout необходимо указать имя exchange без ключей
            # exchange_type=ExchangeType.topic,
        )
        dlq = self.channel.queue_declare(
            queue=Config.RMQ_DLQ_FAILED_PAINT_BUTTON,
            durable=True,
            arguments={
                "x-message-ttl": Config.RMQ_FAILED_PAINT_BUTTON_RETRY_SEC,
                "x-dead-letter-exchange": Config.RMQ_EXCHANGE_PAINT_BUTTON,
                "x-dead-letter-routing-key": Config.RMQ_QUEUE_PAINT_BUTTON,
            },
        )
        self.channel.queue_bind(
            queue=dlq.method.queue,
            exchange=Config.RMQ_DLX_FAILED_PAINT_BUTTON,
            # routing_key=Config.RMQ_DLQ_FAILED_PAINT_BUTTON,         # важно для topic
        )
        log.info("Created dlq: %s", dlq.method.queue)
        return dlq.method.queue

    def declare_main_queue(self) -> str:
        self.channel.exchange_declare(
            exchange=Config.RMQ_EXCHANGE_PAINT_BUTTON,
            exchange_type=ExchangeType.direct,
        )
        paint_queue = self.channel.queue_declare(
            queue=Config.RMQ_QUEUE_PAINT_BUTTON,
            durable=True,
            arguments={
                "x-dead-letter-exchange": Config.RMQ_DLX_FAILED_PAINT_BUTTON,
                # "x-dead-letter-routing-key": Config.RMQ_DEAD_LETTER_KEY,          # важно для topic
            },
        )
        self.channel.queue_bind(
            queue=Config.RMQ_QUEUE_PAINT_BUTTON,
            exchange=Config.RMQ_EXCHANGE_PAINT_BUTTON,
            routing_key=Config.RMQ_QUEUE_PAINT_BUTTON,
        )

        log.info("Declare Queue: %s", paint_queue.method.queue)
        return paint_queue.method.queue

    def declare_queue(self) -> None:
        self.declare_nsq()
        self.declare_dlq()
        self.declare_main_queue()

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
            queue=Config.RMQ_QUEUE_PAINT_BUTTON,
            on_message_callback=message_callback,
            # auto_ack = True,
        )
        log.warning("Waiting for paint_button_tasks")
        self.channel.start_consuming()


class PaintRabbit(PaintRabbitMixin, RabbitBase):
    pass
