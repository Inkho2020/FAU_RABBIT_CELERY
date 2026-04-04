import logging
from datetime import datetime
from time import time

from RMQ_pika_config import (
    config_logging,
    RMQ_EXCHANGE,
    RMQ_ROUTING_KEY,
)

from rabbit.common.simple_exchanger import SimpleRabbit

log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


class Publisher(SimpleRabbit):
    def produce_message(self, idx: int) -> None:
        message_body = f"New message No. {idx:02d}"
        self.channel.basic_publish(
            exchange=RMQ_EXCHANGE,
            routing_key=RMQ_ROUTING_KEY,
            body=message_body,
        )
        log.warning("Published message %s", message_body)


def main():
    config_logging(level=logging.INFO)
    with Publisher() as publisher:
        publisher.declare_queue()
        for idx in range(1, 15):
            publisher.produce_message(idx=idx)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
