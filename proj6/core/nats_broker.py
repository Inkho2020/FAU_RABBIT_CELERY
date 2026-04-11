__all__ = [
    "fs_broker",
    "user_register",
]

from faststream.nats import NatsBroker

from core import settings

fs_broker = NatsBroker(str(settings.nats.nats_url))

user_register = fs_broker.publisher("users.{user_id}.create")
# user_register = fs_broker.publisher("users.#.create")
# решетка "#" в RabbitMQ - ноль и более слов
# звездочка "*" в NATS и в RabbitMQ - ровно одно слово
