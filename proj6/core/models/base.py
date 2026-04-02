from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, declared_attr
from sqlalchemy import Integer


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __table_name__(cls) -> str:
        return f"{cls.__name__}.lower()s"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
