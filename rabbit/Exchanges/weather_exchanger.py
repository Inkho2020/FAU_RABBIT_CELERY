"""
- declare exchange for email....
- bind queue
- start consumer messaging
"""

import logging

from typing import TYPE_CHECKING, Callable


from rabbit.base import RabbitBase
from rabbit import RMQ_config as Config

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import (
        Basic,
        BasicProperties,
    )

log = logging.getLogger(__name__)


class WeatherRabbitMixin:
    channel: "BlockingChannel"

    def publish_message(
        self,
        text: str,
        exchange: str = Config.RMQ_EXCHANGE,
        routing_key: str = Config.RMQ_WEATHER_UPDATE_QUEUE_KEY,
    ) -> None:

        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=text,
            # properties=BasicProperties(
            #     expiration=Config.RMQ_WEATHER_TTL_PROPERTY,
            # ),
        )
        log.info("Published message %s", text)

    def declare_queue(self) -> None:
        dlq = self.channel.queue_declare(
            queue=Config.RMQ_DLQ_WEATHER_QUEUE_KEY,
            durable=True,
            arguments={
                "x-message-ttl": Config.RMQ_DLQ_WEATHER_TTL_KEY,
            },
        )
        log.warning(
            "Declare DLQ %s",
            dlq.method.queue,
        )
        weather_queue = self.channel.queue_declare(
            queue=Config.RMQ_WEATHER_UPDATE_QUEUE_KEY,
            durable=True,
            arguments={
                "x-message-ttl": Config.RMQ_WEATHER_TTL_KEY,
                "x-dead-letter-exchange": Config.RMQ_EXCHANGE,
                "x-dead-letter-routing-key": Config.RMQ_DLQ_WEATHER_QUEUE_KEY,
            },
        )
        log.warning(
            "Declare weather queue %s",
            weather_queue.method.queue,
        )

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
        queue_name: str = Config.RMQ_WEATHER_UPDATE_QUEUE_KEY,
    ):
        self.channel.basic_qos(prefetch_count=prefetch_count)
        self.declare_queue()
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=message_callback,
            # auto_ack = True,
        )
        log.warning("Waiting for messages")
        self.channel.start_consuming()


class WeatherRabbit(WeatherRabbitMixin, RabbitBase):
    pass
