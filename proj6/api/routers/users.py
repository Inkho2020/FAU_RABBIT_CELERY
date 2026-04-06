from fastapi import APIRouter, Depends, BackgroundTasks

from ..routers.fau import fastapi_users
from ..crud.user_crud import (
    create_user_data,
    get_current_user,
)
from core import UserRead, UserUpdate, db_session
from utils.send_welcome_email import send_welcome_email

from typing import TYPE_CHECKING, Annotated

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


@router.put("/my_info")
async def add_user_data(
    session: Annotated[
        "AsyncSession",
        Depends(db_session.get_db),
    ],
    name: str,
    last_name: str,
    background_tasks: BackgroundTasks,
    bio: str | None = None,
    user_id: int = Depends(get_current_user),
):
    user = await create_user_data(
        session=session,
        name=name,
        last_name=last_name,
        bio=bio,
        user_id=user_id,
    )
    background_tasks.add_task(
        send_welcome_email,
        user_id=user_id,
        session=session,
    )
    return user
