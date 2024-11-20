from collections.abc import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)

from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


class Base(DeclarativeBase):
    pass


DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DB_URL)
async_session = async_sessionmaker(engine, class_=AsyncSession)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
