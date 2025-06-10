import pytest
from sqlalchemy import select
from src.models.orders import IndividualOrdersModel
from src.schemas.individual_orders import SIndividualOrderOut, SIndividualOrderIn
from sqlalchemy.exc import IntegrityError, InvalidRequestError

async def create_individual_orders(sessionmaker) -> list[SIndividualOrderOut]:
    test_orders_models = [IndividualOrdersModel(id=1,
                                      username="username_1",
                                      phone="+79999999991",
                                      email="test1@test.ru",
                                      telegram="@test1",
                                      sort=100
                                      ),
                          IndividualOrdersModel(id=2,
                                      username="username_2",
                                      phone="+79999999992",
                                      telegram="@test2",
                                      sort=200
                                      ),
                          IndividualOrdersModel(id=3,
                                      username="username_3",
                                      phone="+79999999993",
                                      email="test3@test.ru",
                                      sort=300
                                      ),
                          IndividualOrdersModel(id=4,
                                      username="username_4",
                                      phone="+79999999994",
                                      sort=400
                                      ),
                          ]
    async with sessionmaker() as session:
        for order in test_orders_models:
            session.add(order)
        await session.commit()
    test_orders_schemas = [model.to_read_model() for model in test_orders_models]
    return test_orders_schemas

@pytest.fixture
def order_in() -> dict:
    order_in = SIndividualOrderIn(
            username="username_1",
            phone="+79999999991",
            email="test1@test.ru",
            telegram="@test1",
        )
    return order_in.model_dump()


class TestIndividualOrdersGetOne:
    @pytest.mark.asyncio
    async def test_get_one_full(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.get_one(id=1)
        assert result is not None
        assert SIndividualOrderOut.model_validate(result)
        assert result == orders_out[0]

    @pytest.mark.asyncio
    async def test_get_one_no_email(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.get_one(id=2)
        assert result is not None
        assert SIndividualOrderOut.model_validate(result)
        assert result == orders_out[1]

    @pytest.mark.asyncio
    async def test_get_one_no_telegram(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.get_one(id=3)
        assert result is not None
        assert SIndividualOrderOut.model_validate(result)
        assert result == orders_out[2]

    @pytest.mark.asyncio
    async def test_get_one_no_email_no_telegram(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.get_one(id=4)
        assert result is not None
        assert SIndividualOrderOut.model_validate(result)
        assert result == orders_out[3]

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, individual_orders_repository):
        result = await individual_orders_repository.get_one(id=-1)
        assert result is None

class TestIndividualOrdersGetAll:
    @pytest.mark.asyncio
    async def test_get_all_empty(self, individual_orders_repository):
        results = await individual_orders_repository.get_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_get_all_no_empty(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        results = await individual_orders_repository.get_all()
        assert len(results) == 4
        for result, order in zip(results, orders_out):
            assert result == order

    @pytest.mark.asyncio
    async def test_get_all_filtered(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        results = await individual_orders_repository.get_all(filter_by={'username': "username_1"})
        assert len(results) == 1
        assert results[0] == orders_out[0]

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        results = await individual_orders_repository.get_all(order_by='-id')
        assert len(results) == 4
        for result, order in zip(results, reversed(orders_out)):
            assert result == order

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_many(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        results = await individual_orders_repository.get_all(order_by=['-id', 'username'])
        assert len(results) == 4
        for result, order in zip(results, reversed(orders_out)):
            assert result == order

    @pytest.mark.asyncio
    async def test_get_all_incorrect_filtered(self, individual_orders_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await individual_orders_repository.get_all(filter_by={'user': "username_1"})
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "individual_orders" has no property "user"' in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_incorrect_ordered(self, individual_orders_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await individual_orders_repository.get_all(order_by='-qwe')
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "individual_orders" has no property "qwe"' in str(e.value)

class TestIndividualOrdersAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, individual_orders_repository, sessionmaker, order_in):
        order_dict = order_in
        result = await individual_orders_repository.add_one(order_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(IndividualOrdersModel, 1)
        assert SIndividualOrderOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, individual_orders_repository, order_in):
        order_dict = order_in
        first_result = await individual_orders_repository.add_one(order_dict)
        second_result = await individual_orders_repository.add_one(order_dict)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_email(self, individual_orders_repository, order_in):
        order_dict = order_in
        order_dict.pop("email")
        result = await individual_orders_repository.add_one(order_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_tg(self, individual_orders_repository, order_in):
        order_dict = order_in
        order_dict.pop("telegram")
        result = await individual_orders_repository.add_one(order_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_email_no_tg(self, individual_orders_repository, order_in):
        order_dict = order_in
        order_dict.pop("email")
        order_dict.pop("telegram")
        result = await individual_orders_repository.add_one(order_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_username(self, individual_orders_repository, order_in):
        order_dict = order_in
        order_dict.pop('username')
        with pytest.raises(Exception) as e:
            await individual_orders_repository.add_one(order_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: individual_orders.username" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_phone(self, individual_orders_repository, order_in):
        order_dict = order_in
        order_dict.pop('phone')
        with pytest.raises(Exception) as e:
            await individual_orders_repository.add_one(order_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: individual_orders.phone" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_all(self, individual_orders_repository):
        order_dict = {}
        with pytest.raises(Exception) as e:
            await individual_orders_repository.add_one(order_dict)
        assert e.type == IntegrityError

class TestIndividualOrdersDeleteOne:
    @pytest.mark.asyncio
    async def test_delete_one(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.delete_one(id = orders_out[0].id)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            stmt = select(IndividualOrdersModel)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 3
        assert orders_out[0] not in orders
        for order, order_out in zip(orders, orders_out[1:]):
            assert order == order_out

    @pytest.mark.asyncio
    async def test_delete_one_not_existing(self, individual_orders_repository, sessionmaker):
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.delete_one(id=-1)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(IndividualOrdersModel)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 4
        assert orders_out[0] in orders
        for order, order_out in zip(orders, orders_out):
            assert order == order_out

class TestIndividualOrdersUpdateOne:
    @pytest.mark.asyncio
    async def test_update_one_full(self, individual_orders_repository, sessionmaker, order_in):
        order_dict = order_in
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.update_one(id = 4, data=order_dict)
        assert result is not None
        assert result == 4
        async with sessionmaker() as session:
            res_one = await session.get(IndividualOrdersModel, 4)
        orders_out[3] = res_one.to_read_model()
        async with sessionmaker() as session:
            stmt = select(IndividualOrdersModel)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, order in zip(results, orders_out):
            assert result == order

    @pytest.mark.asyncio
    async def test_update_one_empty(self, individual_orders_repository, sessionmaker, order_in):
        order_dict = {}
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.update_one(id=4, data=order_dict)
        assert result is not None
        assert result == 4
        async with sessionmaker() as session:
            stmt = select(IndividualOrdersModel)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, order in zip(results, orders_out):
            assert result == order

    @pytest.mark.asyncio
    async def test_update_one_not_existing(self, individual_orders_repository, sessionmaker, order_in):
        order_dict = order_in
        orders_out = await create_individual_orders(sessionmaker)
        result = await individual_orders_repository.update_one(id=-1, data=order_dict)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(IndividualOrdersModel)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, order in zip(results, orders_out):
            assert result == order