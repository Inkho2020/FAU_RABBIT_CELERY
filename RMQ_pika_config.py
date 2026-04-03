import logging

import pika

RMQ_HOST = "localhost"
RMQ_PORT = 5672

RMQ_USER = "wohus"
RMQ_PASS = "pass"

RMQ_EXCHANGE = ""
RMQ_ROUTING_KEY = "hello"


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


def config_logging(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(funcName)10s:%(module)s:%(lineno)-3d %(levelname)-7s - %(message)s",
    )
