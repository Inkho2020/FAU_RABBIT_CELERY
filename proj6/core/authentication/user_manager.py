import logging

from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    models,
)
from fastapi_users.db import BaseUserDatabase

from utils_email_jinja.send_email_confirmation import send_email_confirmation
from utils_email_jinja.send_verification_email import send_verification_email
from ..models.users_model import User
from ..config import UserIDType, settings

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from fastapi import Request, BackgroundTasks
    from fastapi_users.password import PasswordHelperProtocol


log = logging.getLogger(__name__)


class UserManager(IntegerIDMixin, BaseUserManager[User, UserIDType]):
    reset_password_token_secret = settings.access_token.reset_password_token
    verification_token_secret = settings.access_token.verification_token

    def __init__(
        self,
        user_db: BaseUserDatabase[User, UserIDType],
        password_helper: Optional["PasswordHelperProtocol"] = None,
        background_tasks: Optional["BackgroundTasks"] = None,
    ):
        super().__init__(user_db, password_helper)
        self.background_tasks = background_tasks

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
        # verification_link = "http://localhost:8001/docs#/AUTH/verify_verify_v1_auth_verify_post"
        verification_link = request.url_for("verify-email").replace_query_params(
            token=token
        )
        self.background_tasks.add_task(
            send_verification_email,
            user=user,
            verification_link=str(verification_link),
            # verification_link=verification_link,
            # verification_token=token,
        )

    async def on_after_verify(
        self, user: User, request: Optional["Request"] = None
    ) -> None:
        print(f"User{user.id} has been verified")
        log.warning(
            "User %r has been verified.",
            user.id,
        )
        self.background_tasks.add_task(
            send_email_confirmation,
            user=user,
        )

    async def on_after_forgot_password(
        self, user: models.UP, token: str, request: Optional["Request"] = None
    ) -> None:
        log.warning(
            "User %r forgot their password. Reset token: %r",
            user.id,
            token,
        )
