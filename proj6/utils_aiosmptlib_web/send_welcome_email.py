from sqlalchemy.ext.asyncio import AsyncSession

from .send_email import send_email
from core import User


async def send_welcome_email(
    user: User,
):
    topic = f"Welcome, {user.user_data.name}"
    letter_body = f"Dear, {user.user_data.name}, \n\nThank you for choosing our service"

    await send_email(
        recipient=user.email,
        subject=topic,
        body=letter_body,
    )
