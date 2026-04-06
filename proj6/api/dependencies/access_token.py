from fastapi import Depends
from ...core.database import db_session
from ...core.models.access_token_model import AccessToken

from typing import TYPE_CHECKING, Annotated

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_access_token_db(
    session: Annotated[
        "AsyncSession",
        Depends(db_session.get_db),
    ],
):
    yield AccessToken.get_token_db(session=session)
