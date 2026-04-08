"""
- declare exchange for email....
- bind queue
- start consumer messaging
"""

import logging

from typing import TYPE_CHECKING, Callable
from pika.exchange_type import ExchangeType

from rabbit.base import RabbitBase
import rabbit.RMQ_config as Config

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import (
        Basic,
        BasicProperties,
    )

log = logging.getLogger(__name__)


class EmailUpdatesRabbitMixin:
    channel: "BlockingChannel"

    def declare_email_update_exchange(
        self,
    ) -> None:
        self.channel.exchange_declare(
            exchange=Config.RMQ_EMAIL_UPDATES_EXCHANGE_NAME,
            exchange_type=ExchangeType.fanout,
        )

    def declare_queue_for_email_updates(
        self,
        queue_name: str = "",   # Config.RMQ_Exchange
        exclusive: bool = True,
        durable: bool = False,
        auto_delete: bool = True,
    ) -> str:
        self.declare_email_update_exchange()
        queue = self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive,
            # exclusive создает уникальное случайное имя в рамках текущего connection и текущего channel
            # имя мы передаем пустой строчкой, но exclusive генерирует новое имя.
            # МОЖНО ЗАДАТЬ ИМЯ ОЧЕРЕДИ В ОБМЕННИКЕ ПРИ ВЫЗОВЕ consumer_message
            # очередь живет, пока живет текущий канал
            durable=durable,
            auto_delete=auto_delete,
        )
        q_name = queue.method.queue  # тут генерируется новое имя
        self.channel.queue_bind(
            exchange=Config.RMQ_EMAIL_UPDATES_EXCHANGE_NAME,
            queue=q_name,
        )
        return q_name

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
        queue_name: str = "",
        prefetch_count: int = 1,
    ):
        self.channel.basic_qos(prefetch_count=prefetch_count)

        if not queue_name:
            q_name = self.declare_queue_for_email_updates(
                queue_name=queue_name,
            )
        else:
            q_name = self.declare_queue_for_email_updates(
                queue_name=queue_name,
                exclusive=False,  # exclusive if not queue_name
                durable=True,
                auto_delete=False,
            )
        self.channel.basic_consume(
            queue=q_name,
            on_message_callback=message_callback,
        )
        log.warning("Waiting for messages")
        self.channel.start_consuming()


class EmailUpdatesRabbit(EmailUpdatesRabbitMixin, RabbitBase):
    pass
