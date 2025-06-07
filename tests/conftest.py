import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.models.orders import OrdersModel
from src.utils.database import Base
from src.utils.repository import SQLAlchemyRepository
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

@pytest.fixture
def setup_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    async def delete_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    asyncio.run(create_tables())
    yield engine
    asyncio.run(delete_tables())


@pytest.fixture
def sessionmaker(setup_db):
    engine = setup_db
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture
def orders_repository(sessionmaker):
    class TestOrdersRepository(SQLAlchemyRepository):
        model = OrdersModel
    return TestOrdersRepository(sessionmaker)