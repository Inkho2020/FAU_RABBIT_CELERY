from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from typing import AsyncGenerator

from .config import settings


class DBHelper:
    def __init__(self, url, echo, max_overflow, pool_size):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            max_overflow=max_overflow,
            pool_size=pool_size,
        )
        self.session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as session:
            yield session


db_session = DBHelper(
    url=settings.db.url,
    echo=settings.db.echo,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size,
)
