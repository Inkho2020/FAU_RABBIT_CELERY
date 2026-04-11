import logging
from typing import Annotated

from faststream import Depends, Path
from faststream.nats import NatsRouter
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_session, User
from api.crud.user_crud import get_user
from utils_email_jinja.send_welcome_email import send_welcome_email as send_welcome

router = NatsRouter()

log = logging.getLogger(__name__)


@router.subscriber("users.{user_id}.create")
async def send_welcome_nats_email(
    user_id: Annotated[int, Path()],
    session: Annotated[
        AsyncSession,
        Depends(db_session.get_db),
    ],
    msg: str,
) -> None:
    """
    Handles user data registration:
       - Send welcome email.
       - Writes logs
    """
    log.info(
        "Send welcome nats email to user # %d, also msg = %r",
        user_id,
        msg,
    )
    user: User = await get_user(session=session, user_id=user_id)
    await send_welcome(user=user)
