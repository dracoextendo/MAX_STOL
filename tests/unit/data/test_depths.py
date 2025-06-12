import pytest
from sqlalchemy import select
from src.models.products import Depth
from src.schemas.desk_settings import SDepthIn, SDepthOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError

async def create_depths(sessionmaker) -> list[SDepthOut]:
    test_depths_models = [Depth(id=1,
                                  value=10,
                                  sort=100
                                  ),
                           Depth(id=2,
                                  value=20,
                                  sort=200
                                  ),
                           Depth(id=3,
                                  value=30,
                                  sort=300
                                  ),
                          ]
    async with sessionmaker() as session:
        for depth in test_depths_models:
            session.add(depth)
        await session.commit()
    test_depths_schemas = [model.to_read_model() for model in test_depths_models]
    return test_depths_schemas

@pytest.fixture
def depth_in() -> dict:
    depth_in = SDepthIn(value=10,
                              sort=100
                              )
    return depth_in.model_dump()


class TestDepthsGetOne:
    @pytest.mark.asyncio
    async def test_get_one(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.get_one(id=1)
        assert result is not None
        assert SDepthOut.model_validate(result)
        assert result == depths_out[0]

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, depths_repository):
        result = await depths_repository.get_one(id=-1)
        assert result is None

class TestDepthsGetAll:
    @pytest.mark.asyncio
    async def test_get_all_empty(self, depths_repository):
        results = await depths_repository.get_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_get_all_no_empty(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        results = await depths_repository.get_all()
        assert len(results) == 3
        for result, depth in zip(results, depths_out):
            assert result == depth

    @pytest.mark.asyncio
    async def test_get_all_filtered(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        results = await depths_repository.get_all(filter_by={'value': 10})
        assert len(results) == 1
        assert results[0] == depths_out[0]

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        results = await depths_repository.get_all(order_by='-id')
        assert len(results) == 3
        for result, depth in zip(results, reversed(depths_out)):
            assert result == depth

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_many(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        results = await depths_repository.get_all(order_by=['-id', 'value'])
        assert len(results) == 3
        for result, depth in zip(results, reversed(depths_out)):
            assert result == depth

    @pytest.mark.asyncio
    async def test_get_all_incorrect_filtered(self, depths_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await depths_repository.get_all(filter_by={'user': "username_1"})
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "depth" has no property "user"' in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_incorrect_ordered(self, depths_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await depths_repository.get_all(order_by='-qwe')
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "depth" has no property "qwe"' in str(e.value)

class TestDepthsAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, depths_repository, sessionmaker, depth_in):
        depth_dict = depth_in
        result = await depths_repository.add_one(depth_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(Depth, 1)
        assert SDepthOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, depths_repository, depth_in):
        depth_dict = depth_in
        first_result = await depths_repository.add_one(depth_dict)
        second_result = await depths_repository.add_one(depth_dict)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_value(self, depths_repository, depth_in):
        depth_dict = depth_in
        depth_dict.pop('value')
        with pytest.raises(Exception) as e:
            await depths_repository.add_one(depth_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: depth.value" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_sort(self, depths_repository, depth_in):
        depth_dict = depth_in
        depth_dict.pop('sort')
        result = await depths_repository.add_one(depth_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_all(self, depths_repository):
        depth_dict = {}
        with pytest.raises(Exception) as e:
            await depths_repository.add_one(depth_dict)
        assert e.type == IntegrityError

class TestDepthsDeleteOne:
    @pytest.mark.asyncio
    async def test_delete_one(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.delete_one(id = depths_out[0].id)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            stmt = select(Depth)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 2
        assert depths_out[0] not in orders
        for depth, order_out in zip(orders, depths_out[1:]):
            assert depth == order_out

    @pytest.mark.asyncio
    async def test_delete_one_not_existing(self, depths_repository, sessionmaker):
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.delete_one(id=-1)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(Depth)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 3
        assert depths_out[0] in orders
        for depth, order_out in zip(orders, depths_out):
            assert depth == order_out

class TestDepthsUpdateOne:
    @pytest.mark.asyncio
    async def test_update_one_full(self, depths_repository, sessionmaker, depth_in):
        depth_dict = depth_in
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.update_one(id = 3, data=depth_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            res_one = await session.get(Depth, 3)
        depths_out[2] = res_one.to_read_model()
        async with sessionmaker() as session:
            stmt = select(Depth)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, depth in zip(results, depths_out):
            assert result == depth

    @pytest.mark.asyncio
    async def test_update_one_empty(self, depths_repository, sessionmaker):
        depth_dict = {}
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.update_one(id=3, data=depth_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            stmt = select(Depth)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, depth in zip(results, depths_out):
            assert result == depth

    @pytest.mark.asyncio
    async def test_update_one_not_existing(self, depths_repository, sessionmaker, depth_in):
        depth_dict = depth_in
        depths_out = await create_depths(sessionmaker)
        result = await depths_repository.update_one(id=-1, data=depth_dict)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(Depth)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, depth in zip(results, depths_out):
            assert result == depth