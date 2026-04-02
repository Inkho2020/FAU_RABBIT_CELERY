from fastapi import APIRouter
from api.routers.fau import fastapi_users
from core import UserRead, UserUpdate

router = APIRouter(
    tags=["USERS"],
    prefix="/users",
)


# /me
# /{id}
router.include_router(router=fastapi_users.get_users_router(UserRead, UserUpdate))
