import logging
from typing import Annotated

from taskiq import TaskiqDepends
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.user_crud import get_user
from core import db_session, broker, User
from utils_aiosmptlib.send_welcome_email import send_welcome_email as send

log = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(
    user_id: int,
    session: Annotated[
        AsyncSession,
        TaskiqDepends(db_session.get_db),
    ],
):
    user: User = await get_user(session=session, user_id=user_id)
    log.info(
        "Sending welcome email to user %s",
        user_id,
    )
    await send(
        user,
    )
