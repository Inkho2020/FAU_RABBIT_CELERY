from fastapi import (
    APIRouter,
    Depends,
    Request,
)

# from fastapi import BackgroundTask

from core.authentication.fau import fastapi_users
from ..crud.user_crud import (
    update_user_data,
    # get_current_user_id,
    get_current_user_id_from_cookie,
    get_all_users,
)
from core import UserRead, UserUpdate, db_session
from core.nats_broker import user_register

# from core.authentication.fau import current_active_user

# from utils_email_jinja.send_welcome_email import send_welcome_email    для прямой работы нужен Backgroundtask
from utils_email_jinja.web_template import templates

# from taskiq_tasks import send_welcome_email

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
    name: str | None = None,
    last_name: str | None = None,
    # background_tasks: BackgroundTasks,
    bio: str | None = None,
    # user_id: int = Depends(get_current_user_id),  # take user id from bearer/headers token
    user_id: int = Depends(
        get_current_user_id_from_cookie
    ),  # take user information from cookies.
):
    user = await update_user_data(
        session=session,
        name=name,
        last_name=last_name,
        bio=bio,
        user_id=user_id,
    )
    # FASTSTREAM[NATS] TASK
    await user_register.publish(
        subject=f"users.{user_id}.create",
        message=None,
    )

    # TASKIQ TASK
    # await send_welcome_email.kiq(
    #     user_id=user_id,
    # )

    # FASTAPI BACKGROUND TASK
    # background_tasks.add_task(
    #     send_welcome_email,
    #     user_id=user_id,
    #     session=session,
    # )
    return user


@router.get("/", name="users:list")
async def users_list(
    request: Request,
    session: Annotated[
        "AsyncSession",
        Depends(db_session.get_db),
    ],
):
    query = await get_all_users(session)
    return templates.TemplateResponse(
        request=request,
        name="users.html",
        context={"users": query},
    )
