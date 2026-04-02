from fastapi import APIRouter

from core import authentication_backend
from core import UserRead, UserCreate
from core.authentication.user_manager import fastapi_users

router = APIRouter(
    tags=["AUTH"],
    prefix="/auth",
)

# /register
router.include_router(
    router=fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    ),
)

# /request-verify-token
# /verify
router.include_router(
    router=fastapi_users.get_verify_router(UserRead),
)

# /login
# /logout

router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    ),
)
