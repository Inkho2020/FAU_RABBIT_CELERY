from celery import Celery

celery_app = Celery(
    "celery_broker.celery_app",  # from file name celery_app.py
    broker="amqp://wohus:pass@localhost:5672//",
    backend="rpc://",  # rpc:// for rabbit mq, radis://localhost for Radis
    include=["celery_broker.tasks"],
    broker_connection_retry_on_startup=True,
)
