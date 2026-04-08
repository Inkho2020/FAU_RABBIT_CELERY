"""
CREATE
READ
UPDATE
DELETE
"""

from typing import Annotated, Sequence

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import User, AccessToken, db_session, settings, UserDataCreate
from core.models.users_model import UserData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.api.bearer_token_url)


async def get_all_users(
    session: AsyncSession,
) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user(
    session: AsyncSession,
    user_id: int,
) -> User | None:
    return await session.get(User, user_id)


async def get_current_user_id(
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
    return access_token.user_id


async def create_user_data(
    session: AsyncSession,
    name: str,
    last_name: str,
    bio: str | None,
    user_id: int,
):
    payload = {
        "name": name,
        "last_name": last_name,
        "bio": bio,
        "user_id": user_id,
    }
    user_data = UserDataCreate(**payload)

    user_data = UserData(**user_data.model_dump())
    session.add(user_data)
    await session.commit()
    user = await session.get(User, user_id)

    return user
