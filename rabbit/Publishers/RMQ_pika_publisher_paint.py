import logging
from datetime import datetime
from time import time, sleep, strftime

from rabbit.RMQ_config import (
    config_logging,
)

from rabbit.Exchanges import PaintRabbit

log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


class Publisher(PaintRabbit):
    def produce_message(self, idx: int) -> None:
        message_body = f"Paint button # {idx:02d}"
        self.publish_message(message_body)


def main():
    config_logging(level=logging.INFO)
    with Publisher() as publisher:
        publisher.declare_queue()
        for idx in range(1, 50):
            publisher.produce_message(idx=idx)
            sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
