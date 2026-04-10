from fastapi import APIRouter

from ..dependencies.backend import authentication_backend
from core import UserRead, UserCreate, settings
from core.authentication.fau import fastapi_users

router = APIRouter(
    tags=["AUTH"],
    prefix=settings.api.auth,
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
    router=fastapi_users.get_verify_router(
        UserRead,
    ),
)
# /login
# /logout
router.include_router(
    router=fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=False,
    ),
)

# /forgot-password
# /reset-password
router.include_router(
    router=fastapi_users.get_reset_password_router(),
)
