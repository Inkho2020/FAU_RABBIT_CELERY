import random
import string

from .tasks import send_newsletters


def fetch_user_ids():
    return [random.randint(10, 150) for _ in range(random.randint(20, 40))]


def send_newsletters_task():
    # send_newsletters.delay()                    # только если обернуто в celery.app
    user_ids = fetch_user_ids()
    sale_id = random.randint(50, 100)
    promo_code = "".join(random.choices(string.ascii_letters, k=5))

    result = send_newsletters(
        user_ids=user_ids,
        sale_id=sale_id,
        promo_code=promo_code,
    )
    print(result, repr(result))
