from pydantic import BaseModel, ConfigDict, constr
from ..config import UserIDType
from fastapi_users import schemas


class UserDataBase(BaseModel):
    name: constr(min_length=1, max_length=120) | None = None
    last_name: constr(min_length=1, max_length=320) | None = None
    bio: str | None = None


class UserDataCreate(UserDataBase):
    user_id: int


class UserDataUpdate(UserDataBase):
    pass


class UserDataRead(UserDataBase):
    model_config = ConfigDict(from_attributes=True)
    pass


class UserRead(schemas.BaseUser[UserIDType]):
    model_config = ConfigDict(from_attributes=True)
    user_data: UserDataRead | None = None


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    # user_data: UserDataCreate
    pass


class UserRegisteredNotification(BaseModel):
    user: UserRead
    time: int
