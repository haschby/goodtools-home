import pytest
import pytest_asyncio
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from domain.models.baseModel import BaseMain
from domain.models.buyback import Buyback


@pytest_asyncio.fixture
async def session_factory():
    """In-memory SQLite session factory used as the DB test double.

    A single shared in-memory connection is kept alive for the duration of the
    test so schema and data persist across sessions.
    """
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        # Only create the buyback table; other models rely on Postgres-only
        # types (e.g. JSONB) that SQLite cannot compile.
        await conn.run_sync(
            BaseMain.metadata.create_all, tables=[Buyback.__table__]
        )

    factory = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    yield factory

    await engine.dispose()
