from fastapi_users.authentication import AuthenticationBackend

from core.authentication.transport import (
    bearer_transport,  # нужно в ручную получать токент
    cookie_transport,  # токен можно достать из заголовков ?????
)
from .strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="access-token-db",
    # transport=bearer_transport,
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
