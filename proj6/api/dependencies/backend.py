from fastapi_users.authentication import AuthenticationBackend

from core.authentication.transport import (
    # bearer_transport,  # token: Annotated[str, Depends(oauth2_scheme),]
    cookie_transport,  # token: str = request.cookies.get("fastapiusersauth")
)
from .strategy import get_database_strategy

authentication_backend = AuthenticationBackend(
    name="access-token-db",
    # transport=bearer_transport,
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
