from typing import Any

from sqladmin import ModelView
from starlette.requests import Request
from fastapi_users.password import PasswordHelper

from core import User

password_helper = PasswordHelper()


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.email,
        # User.hashed_password,
        User.is_active,
        User.is_superuser,
        User.is_verified,
        User.tokens,
    ]
    column_labels = {User.hashed_password: "Password"}
    form_excluded_columns = [User.tokens]

    async def on_model_change(
        self,
        data: dict,
        model: User,
        is_created: bool,
        request: Request,
    ) -> None:
        raw_password = data.get("hashed_password") or password_helper.generate()
        if is_created or model.hashed_password != raw_password:
            data.update(
                hashed_password=password_helper.hash(raw_password),
            )
