from fastapi import APIRouter
from routers.auth import router as auth_router
from routers.users import router as user_router

router = APIRouter(prefix="v1")

router.include_router(auth_router)
router.include_router(user_router)
