"""
CREATE
READ
UPDATE
DELETE
"""

from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core import User, AccessToken, db_session
from ...core.models.users_model import UserData
from ...core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.bearer_token_url)


async def get_current_user(
    session: Annotated[
        AsyncSession,
        Depends(db_session.get_db),
    ],
    token: Annotated[
        str,
        Depends(oauth2_scheme),
    ],
):
    query = select(AccessToken).where(AccessToken.token == token)
    result = await session.execute(query)
    access_token = result.scalar_one_or_none()
    if not access_token:
        return None
    return int(access_token.user_id)


async def create_user_data(
    name: str,
    last_name: str,
    bio: str,
    session: AsyncSession,
    user_id: int,
):
    query = await session.execute(select(User).where(User.id == user_id))
    user = query.scalar_one_or_none()

    user_data = UserData(
        name=name,
        last_name=last_name,
        bio=bio,
    )
    session.add(user_data)
    await session.commit()
    await session.refresh(user)

    return user
