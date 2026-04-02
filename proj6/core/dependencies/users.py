from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from core.database import db_session
from core.models.users_model import User

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_users_db(
    session: Annotated["AsyncSession", Depends(db_session.get_db)],
):
    yield User.get_user_db(session=session)