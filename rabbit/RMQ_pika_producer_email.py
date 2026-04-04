import logging
from datetime import datetime
from time import time

from rabbit.common import EmailUpdatesRabbit

from RMQ_pika_config import (
    config_logging,
    RMQ_EMAIL_UPDATES_EXCHANGE_NAME,
)

log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


class Producer(EmailUpdatesRabbit):
    def produce_message(self, idx: int) -> None:
        message_body = f"New message No. {idx:02d}"
        self.channel.basic_publish(
            exchange=RMQ_EMAIL_UPDATES_EXCHANGE_NAME,
            routing_key="",
            body=message_body,
        )
        log.warning("Published message %s", message_body)


def main():
    config_logging()
    with Producer() as producer:
        producer.declare_email_update_exchange()
        for idx in range(1, 6):
            producer.produce_message(idx=idx)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
