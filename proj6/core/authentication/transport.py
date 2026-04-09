from fastapi_users.authentication import (
    BearerTransport,
    CookieTransport,
)

from ..config import settings

bearer_transport = BearerTransport(
    tokenUrl=settings.api.bearer_token_url,
)
cookie_transport = CookieTransport(
    cookie_max_age=3600,
    cookie_secure=False,
)
