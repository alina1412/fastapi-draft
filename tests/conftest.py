import warnings
from os import environ
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)

from service.__main__ import app
from service.db_setup.db_settings import get_session
from service.db_setup.models import Base

from .fixtures import *

warnings.filterwarnings("ignore", category=DeprecationWarning)


TEST_DB_URL = environ.get(
    "TEST_DB_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db",
)


@pytest.fixture(scope="function")
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(TEST_DB_URL, echo=True)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture(scope="function")
async def test_session_factory(
    test_engine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )


@pytest.fixture(scope="function")
async def session(
    test_engine: AsyncEngine,
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session_:
        yield session_


@pytest.fixture(scope="function")
async def client(
    test_engine: AsyncEngine,
    test_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncClient, None]:
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def override_get_session():
        async with test_session_factory() as sess:
            yield sess

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as aclient:
        yield aclient

    app.dependency_overrides.clear()
