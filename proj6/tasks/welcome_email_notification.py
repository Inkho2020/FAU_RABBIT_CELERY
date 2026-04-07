import logging
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_session, broker
from utils_aiosmptlib.send_welcome_email import send_welcome_email as send

log = logging.getLogger(__name__)


@broker.task
async def send_welcome_email(
    user_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_session.get_db),
    ],
):
    log.info(
        "Sending welcome email to user %s",
        user_id,
    )
    await send(
        user_id=user_id,
        session=session,
    )
