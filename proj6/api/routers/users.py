from fastapi import APIRouter, Depends

from api.routers.fau import fastapi_users
from api.crud.user_crud import create_user_data, get_current_user
from core import UserRead, UserUpdate, db_session

from sqlalchemy.ext.asyncio import AsyncSession

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    tags=["USERS"],
    prefix="/users",
)

# /me
# /{id}
router.include_router(
    router=fastapi_users.get_users_router(
        UserRead,
        UserUpdate,
    ),
)


@router.post("/user_data")
async def add_user_data(
    name: str,
    last_name: str,
    session: AsyncSession = Depends(db_session.get_db),
    user_id: int = Depends(get_current_user),
):
    return await create_user_data(
        name=name,
        last_name=last_name,
        session=session,
        user_id=user_id,
    )
