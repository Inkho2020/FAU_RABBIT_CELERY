from pydantic import BaseModel, ConfigDict
from core import UserIDType
from fastapi_users import schemas


class UserDataBase(BaseModel):
    name: str
    last_name: str


class UserDataCreate(UserDataBase):
    pass


class UserDataUpdate(UserDataBase):
    pass


class UserDataRead(UserDataBase):
    model_config = ConfigDict(from_attributes=True)
    pass


class UserRead(schemas.BaseUser[UserIDType]):
    model_config = ConfigDict(from_attributes=True)
    # user_data: UserDataRead


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class UserRegisteredNotification(BaseModel):
    user: UserRead
    time: int
