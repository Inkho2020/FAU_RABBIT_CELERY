from sqlalchemy import String, Text, ForeignKey

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyUserDatabase,
    SQLAlchemyBaseUserTable,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from .base import Base
from .mixins import CreatedAtMixin
from ..config import UserIDType


class User(Base, SQLAlchemyBaseUserTable[UserIDType], CreatedAtMixin):
    pass

    @classmethod
    def get_user_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)

    user_data: Mapped["UserData"] = relationship(
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )


class UserData(Base):
    name: Mapped[str] = mapped_column(String(120))
    last_name: Mapped[str] = mapped_column(String(320))
    bio: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
        nullable=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    owner: Mapped["User"] = relationship(back_populates="user_data")
