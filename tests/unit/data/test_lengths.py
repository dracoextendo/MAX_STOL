import pytest
from sqlalchemy import select
from src.models.products import Length
from src.schemas.desk_settings import SLengthIn, SLengthOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError

async def create_lengths(sessionmaker) -> list[SLengthOut]:
    test_lengths_models = [Length(id=1,
                                  value=10,
                                  sort=100
                                  ),
                           Length(id=2,
                                  value=20,
                                  sort=200
                                  ),
                           Length(id=3,
                                  value=30,
                                  sort=300
                                  ),
                          ]
    async with sessionmaker() as session:
        for length in test_lengths_models:
            session.add(length)
        await session.commit()
    test_lengths_schemas = [model.to_read_model() for model in test_lengths_models]
    return test_lengths_schemas

@pytest.fixture
def length_in() -> dict:
    length_in = SLengthIn(value=10,
                              sort=100
                              )
    return length_in.model_dump()


class TestLengthsGetOne:
    @pytest.mark.asyncio
    async def test_get_one(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.get_one(id=1)
        assert result is not None
        assert SLengthOut.model_validate(result)
        assert result == lengths_out[0]

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, lengths_repository):
        result = await lengths_repository.get_one(id=-1)
        assert result is None

class TestLengthsGetAll:
    @pytest.mark.asyncio
    async def test_get_all_empty(self, lengths_repository):
        results = await lengths_repository.get_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_get_all_no_empty(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        results = await lengths_repository.get_all()
        assert len(results) == 3
        for result, length in zip(results, lengths_out):
            assert result == length

    @pytest.mark.asyncio
    async def test_get_all_filtered(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        results = await lengths_repository.get_all(filter_by={'value': 10})
        assert len(results) == 1
        assert results[0] == lengths_out[0]

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        results = await lengths_repository.get_all(order_by='-id')
        assert len(results) == 3
        for result, length in zip(results, reversed(lengths_out)):
            assert result == length

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_many(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        results = await lengths_repository.get_all(order_by=['-id', 'value'])
        assert len(results) == 3
        for result, length in zip(results, reversed(lengths_out)):
            assert result == length

    @pytest.mark.asyncio
    async def test_get_all_incorrect_filtered(self, lengths_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await lengths_repository.get_all(filter_by={'user': "username_1"})
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "length" has no property "user"' in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_incorrect_ordered(self, lengths_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await lengths_repository.get_all(order_by='-qwe')
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "length" has no property "qwe"' in str(e.value)

class TestLengthsAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, lengths_repository, sessionmaker, length_in):
        length_dict = length_in
        result = await lengths_repository.add_one(length_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(Length, 1)
        assert SLengthOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, lengths_repository, length_in):
        length_dict = length_in
        first_result = await lengths_repository.add_one(length_dict)
        second_result = await lengths_repository.add_one(length_dict)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_value(self, lengths_repository, length_in):
        length_dict = length_in
        length_dict.pop('value')
        with pytest.raises(Exception) as e:
            await lengths_repository.add_one(length_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: length.value" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_sort(self, lengths_repository, length_in):
        length_dict = length_in
        length_dict.pop('sort')
        result = await lengths_repository.add_one(length_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_all(self, lengths_repository):
        length_dict = {}
        with pytest.raises(Exception) as e:
            await lengths_repository.add_one(length_dict)
        assert e.type == IntegrityError

class TestLengthsDeleteOne:
    @pytest.mark.asyncio
    async def test_delete_one(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.delete_one(id = lengths_out[0].id)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            stmt = select(Length)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 2
        assert lengths_out[0] not in orders
        for length, order_out in zip(orders, lengths_out[1:]):
            assert length == order_out

    @pytest.mark.asyncio
    async def test_delete_one_not_existing(self, lengths_repository, sessionmaker):
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.delete_one(id=-1)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(Length)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 3
        assert lengths_out[0] in orders
        for length, order_out in zip(orders, lengths_out):
            assert length == order_out

class TestLengthsUpdateOne:
    @pytest.mark.asyncio
    async def test_update_one_full(self, lengths_repository, sessionmaker, length_in):
        length_dict = length_in
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.update_one(id = 3, data=length_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            res_one = await session.get(Length, 3)
        lengths_out[2] = res_one.to_read_model()
        async with sessionmaker() as session:
            stmt = select(Length)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, length in zip(results, lengths_out):
            assert result == length

    @pytest.mark.asyncio
    async def test_update_one_empty(self, lengths_repository, sessionmaker):
        length_dict = {}
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.update_one(id=3, data=length_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            stmt = select(Length)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, length in zip(results, lengths_out):
            assert result == length

    @pytest.mark.asyncio
    async def test_update_one_not_existing(self, lengths_repository, sessionmaker, length_in):
        length_dict = length_in
        lengths_out = await create_lengths(sessionmaker)
        result = await lengths_repository.update_one(id=-1, data=length_dict)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(Length)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, length in zip(results, lengths_out):
            assert result == length