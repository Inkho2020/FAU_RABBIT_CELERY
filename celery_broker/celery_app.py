from celery import Celery

celery_app = Celery(
    "celery_broker.celery_app",
    broker="amqp://wohus:pass@localhost:5762//",
    backend="rpc://",
)
