from fastapi_users import FastAPIUsers

from ..dependencies.backend import authentication_backend
from ..dependencies.user_manager_depends import get_user_manager
from core import User, UserIDType

fastapi_users = FastAPIUsers[User, UserIDType](
    get_user_manager,
    [authentication_backend],
)
