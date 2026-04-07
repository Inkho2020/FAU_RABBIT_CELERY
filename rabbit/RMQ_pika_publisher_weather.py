import logging
from datetime import datetime
from time import time, sleep, strftime

from RMQ_pika_config import (
    config_logging,
)

from common import WeatherRabbit

log = logging.getLogger(__name__)
record_time = datetime.fromtimestamp(int(time()))


class Publisher(WeatherRabbit):
    def produce_message(self, idx: int) -> None:
        message_body = f"Weather report No. {idx:02d} at {strftime('%H:%M:%S')}"
        self.publish_message(message_body)


def main():
    config_logging(level=logging.INFO)
    with Publisher() as publisher:
        publisher.declare_queue()
        for idx in range(1, 151):
            publisher.produce_message(idx=idx)
            sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.info("Bye")
