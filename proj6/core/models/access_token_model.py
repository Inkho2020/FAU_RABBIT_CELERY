from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from ..config import UserIDType
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .users_model import User


class AccessToken(Base, SQLAlchemyBaseAccessTokenTable[UserIDType]):
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user: Mapped["User"] = relationship(back_populates="tokens")

    @classmethod
    def get_token_db(cls, session: "AsyncSession"):
        return SQLAlchemyAccessTokenDatabase(session, cls)

    def __str__(self):
        return self.token
