from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)
from .base import Base
from core.config import UserIDType


class User(Base, SQLAlchemyBaseUserTable[UserIDType]):
    pass

    @classmethod
    def get_user_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
