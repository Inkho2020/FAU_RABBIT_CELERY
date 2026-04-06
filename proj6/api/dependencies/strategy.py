from fastapi import Depends

from .access_token import get_access_token_db
from core.config import settings
from fastapi_users.authentication.strategy.db import DatabaseStrategy
from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from core.models.access_token_model import AccessToken
    from fastapi_users.authentication.strategy.db import AccessTokenDatabase


async def get_database_strategy(
    access_token_db: Annotated[
        "AccessTokenDatabase[AccessToken]",
        Depends(get_access_token_db),
    ],
) -> DatabaseStrategy:
    return DatabaseStrategy(
        database=access_token_db,
        lifetime_seconds=settings.access_token.lifetime,
    )
