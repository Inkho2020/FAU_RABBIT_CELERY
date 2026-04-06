from pydantic import BaseModel, ConfigDict, constr
from ..config import UserIDType
from fastapi_users import schemas


class UserDataBase(BaseModel):
    name: str | None = constr(min_length=1, max_length=120)
    last_name: str | None = constr(min_length=1, max_length=320)
    bio: str | None = None


class UserDataCreate(UserDataBase):
    pass


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
    user_data: UserDataCreate


class UserRegisteredNotification(BaseModel):
    user: UserRead
    time: int
