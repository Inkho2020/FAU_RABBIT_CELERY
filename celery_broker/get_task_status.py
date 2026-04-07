from celery.result import AsyncResult
from .celery_app import celery_app


def main():
    result = AsyncResult(
        "task_celery_number",
        app=celery_app,
    )
    print(
        result,
        result.status,
        result.name,
        sep="\n",
    )


if __name__ == "__main__":
    main()
