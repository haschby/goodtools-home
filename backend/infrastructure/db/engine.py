from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    async_sessionmaker,
    AsyncSession, 
    AsyncEngine
)
from typing import AsyncGenerator
from sqlalchemy.ext.declarative import DeclarativeMeta

class Database:
    def __init__(self, database_uri: str, extra_args: dict = None):
        self.engine = create_async_engine(
            database_uri,
            echo=False,
            pool_pre_ping=True,
            connect_args=extra_args if extra_args else {},
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
    
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def init_models(self, base: DeclarativeMeta) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

# engine = create_async_engine(
#     settings.database_uri, 
#     echo=False, 
#     pool_pre_ping=True
# )

# AsyncSessionLocal = async_sessionmaker(
#     engine, 
#     expire_on_commit=False,
#     class_=AsyncSession
# )

# async def get_session() -> AsyncGenerator[AsyncSession, None]:
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception:
#             await session.rollback()
#             raise
#         finally:
#             await session.close()

# async def init_models() -> None:
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)