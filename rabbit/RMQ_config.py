import logging

import pika

# DEFAULT_LOG_FORMAT = "%(asctime)s.%(msecs)03d] %(funcName)10s:%(module)s:%(lineno)-3d %(levelname)-7s - %(message)s"
DEFAULT_LOG_FORMAT = "%(module)s:%(lineno)-3d %(levelname)-6s - %(message)s"

RMQ_HOST = "localhost"
RMQ_PORT = 5672

RMQ_USER = "wohus"
RMQ_PASS = "pass"

# Name of main exchange
RMQ_EXCHANGE = ""
# Name of queue / name of key to queue
RMQ_ROUTING_KEY = "Queue_Key"
# specified exchanged name
RMQ_QUEUE_NAME_KYC_EMAIL_UPDATES = "kyc-email-updates"
# name of queue for emails
RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES = "newsletter-email-updates"
# DLQ
RMQ_DEAD_LETTER_EXCHANGE = "dlq-exchange"
RMQ_DEAD_LETTER_KEY = "dlq-messages"

RMQ_EMAIL_UPDATES_EXCHANGE_NAME = "email-updates"
# Exchange for TTL
RMQ_WEATHER_UPDATE_QUEUE_KEY = "q-weather-updates"
# TTL Queue
RMQ_WEATHER_TTL_KEY = 60_000  # TTL of 60 sec
# RMQ_WEATHER_TTL_PROPERTY = "60000"  # TTL of 60 sec
# DLQ Exchange name for TTL
RMQ_DLQ_WEATHER_QUEUE_KEY = "q-expire-weather-updates"
# DLQ TTL QUEUE
RMQ_DLQ_WEATHER_TTL_KEY = 90_000  # TTL of 90 sec

RMQ_EXCHANGE_PAINT_BUTTON = "x-paint-button-taskiq_tasks"
RMQ_QUEUE_PAINT_BUTTON = "q-paint-button-taskiq_tasks"
RMQ_DLX_FAILED_PAINT_BUTTON = "dlx-failed-to-paint-button-taskiq_tasks"
RMQ_DLQ_FAILED_PAINT_BUTTON = "dlq-failed-to-paint-button-taskiq_tasks"
RMQ_FAILED_PAINT_BUTTON_RETRY_SEC = 5_000

RMQ_QUEUE_NOT_SOLVE_TASKS = "not-solved-taskiq_tasks"

connection_params = pika.ConnectionParameters(
    host=RMQ_HOST,
    port=RMQ_PORT,
    credentials=pika.PlainCredentials(
        RMQ_USER,
        RMQ_PASS,
    ),
)


def get_connection() -> pika.BlockingConnection:
    return pika.BlockingConnection(
        parameters=connection_params,
    )


def config_logging(
    level: int = logging.INFO,
    pika_log_level: int = logging.WARNING,
):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=DEFAULT_LOG_FORMAT,
    )
    logging.getLogger("pika").setLevel(pika_log_level)
