import logging

import pika

# DEFAULT_LOG_FORMAT = "%(asctime)s.%(msecs)03d] %(funcName)10s:%(module)s:%(lineno)-3d %(levelname)-7s - %(message)s"
DEFAULT_LOG_FORMAT = "%(module)s:%(lineno)-3d %(levelname)-6s - %(message)s"

RMQ_HOST = "localhost"
RMQ_PORT = 5672

RMQ_USER = "wohus"
RMQ_PASS = "pass"

RMQ_EXCHANGE = ""
RMQ_ROUTING_KEY = "Queue_kye_name"

RMQ_EMAIL_UPDATES_EXCHANGE_NAME = "email-updates"

RMQ_QUEUE_NAME_KYC_EMAIL_UPDATES = "kyc-email-updates"
RMQ_QUEUE_NAME_NEWSLETTER_EMAIL_UPDATES = "newsletter-email-updates"

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
        pika_log_level:int = logging.WARNING,
):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format=DEFAULT_LOG_FORMAT,
    )
    logging.getLogger("pika").setLevel(pika_log_level)
