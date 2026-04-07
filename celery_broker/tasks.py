import random

from utils_aiosmptlib.send_email import send_email


def fetch_user_info(user_ids: list[int]) -> list[tuple[str, str]]:
    return [
        (
            f"User #{user_id:02d}",
            f"user{user_id}@example.com",
        )
        for user_id in user_ids
    ]


newsletter_template = """\
Dear {name},

You won a car.
To get your prise you should registry on our service with promo_code {promo_code}.
Please let our sale manage know sales id {sale_id}.
And make payment 100$ for deliver of your prise.

"""


# @app.task                         если запускать через celery.app
def send_newsletters(
    user_ids: list[int],
    sale_id: int,
    promo_code: str,
):
    users_info = fetch_user_info(user_ids)
    for name, email in users_info:
        recipient = email
        subject = f"{name.title()}, won a PRISE!!!"
        body = newsletter_template.format(
            name=name,
            promo_code=promo_code,
            sale_id=sale_id,
        )

        send_email(
            recipient=recipient,
            subject=subject,
            body=body,
        )
