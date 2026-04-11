"""
CREATE
READ
UPDATE
DELETE
"""

from typing import Annotated, Sequence

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core import User, AccessToken, db_session, settings
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


# take token rom bearer token in headers. For cookies needs another algorithm
# async def get_current_user_id(
#     session: Annotated[
#         AsyncSession,
#         Depends(db_session.get_db),
#     ],
#     token: Annotated[
#         str,
#         Depends(oauth2_scheme),
#     ],
# ):
#     query = select(AccessToken).where(AccessToken.token == token)
#     result = await session.execute(query)
#     access_token = result.scalar_one_or_none()
#     if not access_token:
#         return None
#     return access_token.user_id


async def get_current_user_id_from_cookie(
    request: Request,
    session: Annotated[
        AsyncSession,
        Depends(db_session.get_db),
    ],
):
    # достаём токен из cookie
    token: str = request.cookies.get("fastapiusersauth")
    if not token:
        return None

    query = select(AccessToken).where(AccessToken.token == token)
    result = await session.execute(query)
    access_token = result.scalar_one_or_none()
    if not access_token:
        return None
    return access_token.user_id


def normalize(value: str | None) -> str | None:
    return value.title() if value else None


async def update_user_data(
    session: AsyncSession,
    name: str,
    last_name: str,
    bio: str,
    user_id: int,
):
    user = await get_user(
        session=session,
        user_id=user_id,
    )
    user_info = {
        "name": normalize(name),
        "last_name": normalize(last_name),
        "bio": bio,
    }
    if user.user_data is None:
        user.user_data = UserData(user_id=user_id, **user_info)
    else:
        for key, value in user_info.items():
            if value is None:
                continue
            setattr(user.user_data, key, value)

    await session.commit()
    await session.refresh(user)

    return user
