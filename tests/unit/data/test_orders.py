import pytest
from src.models.orders import OrdersModel
from src.schemas.orders import SOrderOut


async def create_orders(sessionmaker):
    async with sessionmaker() as session:
        test_orders = [OrdersModel(id = 1,
                                   username = "test1",
                                   phone = "+79999999999",
                                   email = "test@test.ru",
                                   telegram = "@testtest",
                                   product_name = "test",
                                   desk_color = "test",
                                   frame_color = "test",
                                   depth = "test",
                                   length = "test",
                                   sort = 1
                                   ),
                       OrdersModel(id=2,
                                   username="test2",
                                   phone="+79999999999",
                                   telegram="@testtest",
                                   product_name="test",
                                   desk_color="test",
                                   frame_color="test",
                                   depth="test",
                                   length="test",
                                   sort=2
                                   ),
                       OrdersModel(id=3,
                                   username="test3",
                                   phone="+79999999999",
                                   email="test@test.ru",
                                   product_name="test",
                                   desk_color="test",
                                   frame_color="test",
                                   depth="test",
                                   length="test",
                                   sort=3
                                   ),
                       OrdersModel(id=4,
                                   username="test4",
                                   phone="+79999999999",
                                   product_name="test",
                                   desk_color="test",
                                   frame_color="test",
                                   depth="test",
                                   length="test",
                                   sort=1
                                   ),
                       ]
        for order in test_orders:
            session.add(order)
        await session.commit()

@pytest.mark.asyncio
async def test_get_one_existing(orders_repository, sessionmaker):
    await create_orders(sessionmaker)
    result = await orders_repository.get_one(id=1)
    assert result is not None
    assert SOrderOut.model_validate(result)
    assert result.id == 1
    assert result.username == "test1"
    assert result.phone == "+79999999999"
    assert result.email == "test@test.ru"
    assert result.telegram == "@testtest"
    assert result.product_name == "test"
    assert result.desk_color == "test"
    assert result.frame_color == "test"
    assert result.depth == "test"
    assert result.length == "test"
    assert result.sort == 1

@pytest.mark.asyncio
async def test_get_one_not_existing(orders_repository):
    result = await orders_repository.get_one(id=1)
    assert result is None