import sys
from pathlib import Path

import pytest_asyncio

sys.path.insert(0, str(Path(__file__).parent.parent))


import pytest
from litestar.testing import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from entities import Base
from main import app
from repositories.order_repository import OrderRepository
from repositories.product_repository import ProductRepository
from repositories.user_repository import UserRepository

TEST_DATABASE_URI = 'sqlite+aiosqlite:///./test.db'

@pytest_asyncio.fixture(scope='session')
def engine():
    return create_async_engine(TEST_DATABASE_URI, echo=True)

@pytest_asyncio.fixture(scope='session')
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session(engine, tables):
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
def user_repository(session):
    return UserRepository(session)

@pytest_asyncio.fixture
def product_repository(session):
    return ProductRepository(session)

@pytest_asyncio.fixture
def order_repository(session):
    return OrderRepository(session)

@pytest_asyncio.fixture
def client():
    return TestClient(app=app)