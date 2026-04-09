from sqlalchemy.ext.asyncio import AsyncSession

from .send_email import send_email
from core import User


async def send_welcome_email(
    user: User,
):
    name = user.user_data.name
    topic = ""
    if not name:
        topic = f"Welcome, {user.user_data.last_name}"
        name = user.user_data.last_name
    elif not user.user_data.last_name:
        topic = f"Welcome, Sir/Madam"
        name = "Sirs"
    letter_body = f"Dear, {name}, \n\nThank you for choosing our service"

    await send_email(
        recipient=user.email,
        subject=topic,
        body=letter_body,
    )
