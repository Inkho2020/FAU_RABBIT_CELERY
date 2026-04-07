import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from rabbit.RMQ_config import connection_params as conn_param


class RabbitException(Exception):
    pass


class RabbitBase:
    def __init__(
        self,
        connection_params: pika.ConnectionParameters = conn_param,
    ) -> None:
        self.connection_params = connection_params
        self._connection: BlockingConnection | None = None
        self._channel: BlockingChannel | None = None

    def get_connection(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(self.connection_params)

    @property
    def channel(self):
        if self._channel is None:
            raise RabbitException
        return self._channel

    def __enter__(self):
        self._connection = self.get_connection()
        self._channel = self._connection.channel()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._channel.is_open:
            self._channel.close()
        if self._connection.is_open:
            self._connection.close()
