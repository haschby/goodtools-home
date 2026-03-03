from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker,
    AsyncSession, 
    AsyncEngine
)
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from domain.models.baseModel import Base
from infrastructure.config.settings import settings

engine = create_async_engine(
    settings.database_uri, 
    echo=False, 
    pool_pre_ping=True
)

AsyncSessionLocal = async_sessionmaker(
    engine, expire_on_commit=False
)

async def init_models() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)