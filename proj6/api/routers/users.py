from fastapi import APIRouter
from core.authentication.user_manager import fastapi_users
from core import UserRead, UserUpdate

router = APIRouter(
    tags=["USERS"],
    prefix="users",
)


# /me
# /{id}
router.include_router(router=fastapi_users.get_users_router(UserRead, UserUpdate))
