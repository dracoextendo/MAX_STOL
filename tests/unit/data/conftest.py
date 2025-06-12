import asyncio
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.repositories.desk_settings import DeskColorsRepository, FrameColorsRepository, LengthRepository, \
    DepthRepository
from src.repositories.individual_orders import IndividualOrdersRepository
from src.repositories.orders import OrdersRepository
from src.repositories.products import ProductsRepository
from src.repositories.users import UsersRepository
from src.utils.database import Base

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
    return OrdersRepository(sessionmaker)

@pytest.fixture
def individual_orders_repository(sessionmaker):
    return IndividualOrdersRepository(sessionmaker)

@pytest.fixture
def desk_colors_repository(sessionmaker):
    return DeskColorsRepository(sessionmaker)

@pytest.fixture
def frame_colors_repository(sessionmaker):
    return FrameColorsRepository(sessionmaker)

@pytest.fixture
def lengths_repository(sessionmaker):
    return LengthRepository(sessionmaker)

@pytest.fixture
def depths_repository(sessionmaker):
    return DepthRepository(sessionmaker)

@pytest.fixture
def users_repository(sessionmaker):
    return UsersRepository(sessionmaker)

@pytest.fixture
def products_repository(sessionmaker):
    return ProductsRepository(sessionmaker)