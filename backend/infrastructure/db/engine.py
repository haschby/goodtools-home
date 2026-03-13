from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker,
    AsyncSession, 
    AsyncEngine
)
from typing import AsyncGenerator
from domain.models.baseModel import Base
from infrastructure.config.settings import settings

engine = create_async_engine(
    settings.database_uri, 
    echo=False, 
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)