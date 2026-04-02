import logging

from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    models,
)

from core.models.users_model import User
from core.config import UserIDType, settings

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIDType]):
    reset_password_token_secret = settings.access_token.reset_password_token
    verification_token_secret = settings.access_token.verification_token

    async def on_after_register(
        self,
        user: User,
        request: Optional["Request"] = None,
    ) -> None:
        log.warning(
            "User %r has registered.",
            user.id,
        )
        # await send_new_user_notification(user)

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional["Request"] = None
    ) -> None:
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )

    async def on_after_forgot_password(
        self, user: models.UP, token: str, request: Optional["Request"] = None
    ) -> None:
        log.warning(
            "User %r forgot their password. Reset token: %r",
            user.id,
            token,
        )
