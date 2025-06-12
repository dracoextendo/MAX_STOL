import pytest
from sqlalchemy import select
from src.models.products import FrameColors
from src.schemas.desk_settings import SFrameColorIn, SFrameColorOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError

async def create_frame_colors(sessionmaker) -> list[SFrameColorOut]:
    test_frame_colors_models = [FrameColors(id=1,
                                          name="name_1",
                                          sort=100
                                      ),
                               FrameColors(id=2,
                                          name="name_2",
                                          sort=200
                                      ),
                               FrameColors(id=3,
                                          name="name_3",
                                          sort=300
                                          ),
                          ]
    async with sessionmaker() as session:
        for frame_color in test_frame_colors_models:
            session.add(frame_color)
        await session.commit()
    test_frame_colors_schemas = [model.to_read_model() for model in test_frame_colors_models]
    return test_frame_colors_schemas

@pytest.fixture
def frame_color_in() -> dict:
    frame_color_in = SFrameColorIn(name="name_1",
                            sort=100
                            )
    return frame_color_in.model_dump()


class TestFrameColorsGetOne:
    @pytest.mark.asyncio
    async def test_get_one(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.get_one(id=1)
        assert result is not None
        assert SFrameColorOut.model_validate(result)
        assert result == frame_colors_out[0]

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, frame_colors_repository):
        result = await frame_colors_repository.get_one(id=-1)
        assert result is None

class TestFrameColorsGetAll:
    @pytest.mark.asyncio
    async def test_get_all_empty(self, frame_colors_repository):
        results = await frame_colors_repository.get_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_get_all_no_empty(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        results = await frame_colors_repository.get_all()
        assert len(results) == 3
        for result, frame_color in zip(results, frame_colors_out):
            assert result == frame_color

    @pytest.mark.asyncio
    async def test_get_all_filtered(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        results = await frame_colors_repository.get_all(filter_by={'name': "name_1"})
        assert len(results) == 1
        assert results[0] == frame_colors_out[0]

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        results = await frame_colors_repository.get_all(order_by='-id')
        assert len(results) == 3
        for result, frame_color in zip(results, reversed(frame_colors_out)):
            assert result == frame_color

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_many(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        results = await frame_colors_repository.get_all(order_by=['-id', 'name'])
        assert len(results) == 3
        for result, frame_color in zip(results, reversed(frame_colors_out)):
            assert result == frame_color

    @pytest.mark.asyncio
    async def test_get_all_incorrect_filtered(self, frame_colors_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await frame_colors_repository.get_all(filter_by={'user': "username_1"})
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "frame_colors" has no property "user"' in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_incorrect_ordered(self, frame_colors_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await frame_colors_repository.get_all(order_by='-qwe')
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "frame_colors" has no property "qwe"' in str(e.value)

class TestFrameColorsAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, frame_colors_repository, sessionmaker, frame_color_in):
        frame_color_dict = frame_color_in
        result = await frame_colors_repository.add_one(frame_color_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(FrameColors, 1)
        assert SFrameColorOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, frame_colors_repository, frame_color_in):
        frame_color_dict = frame_color_in
        first_result = await frame_colors_repository.add_one(frame_color_dict)
        second_result = await frame_colors_repository.add_one(frame_color_dict)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_name(self, frame_colors_repository, frame_color_in):
        frame_color_dict = frame_color_in
        frame_color_dict.pop('name')
        with pytest.raises(Exception) as e:
            await frame_colors_repository.add_one(frame_color_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: frame_colors.name" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_sort(self, frame_colors_repository, frame_color_in):
        frame_color_dict = frame_color_in
        frame_color_dict.pop('sort')
        result = await frame_colors_repository.add_one(frame_color_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_all(self, frame_colors_repository):
        frame_color_dict = {}
        with pytest.raises(Exception) as e:
            await frame_colors_repository.add_one(frame_color_dict)
        assert e.type == IntegrityError

class TestFrameColorsDeleteOne:
    @pytest.mark.asyncio
    async def test_delete_one(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.delete_one(id = frame_colors_out[0].id)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            stmt = select(FrameColors)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 2
        assert frame_colors_out[0] not in orders
        for frame_color, order_out in zip(orders, frame_colors_out[1:]):
            assert frame_color == order_out

    @pytest.mark.asyncio
    async def test_delete_one_not_existing(self, frame_colors_repository, sessionmaker):
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.delete_one(id=-1)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(FrameColors)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 3
        assert frame_colors_out[0] in orders
        for frame_color, order_out in zip(orders, frame_colors_out):
            assert frame_color == order_out

class TestFrameColorsUpdateOne:
    @pytest.mark.asyncio
    async def test_update_one_full(self, frame_colors_repository, sessionmaker, frame_color_in):
        frame_color_dict = frame_color_in
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.update_one(id = 3, data=frame_color_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            res_one = await session.get(FrameColors, 3)
        frame_colors_out[2] = res_one.to_read_model()
        async with sessionmaker() as session:
            stmt = select(FrameColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, frame_color in zip(results, frame_colors_out):
            assert result == frame_color

    @pytest.mark.asyncio
    async def test_update_one_empty(self, frame_colors_repository, sessionmaker):
        frame_color_dict = {}
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.update_one(id=3, data=frame_color_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            stmt = select(FrameColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, frame_color in zip(results, frame_colors_out):
            assert result == frame_color

    @pytest.mark.asyncio
    async def test_update_one_not_existing(self, frame_colors_repository, sessionmaker, frame_color_in):
        frame_color_dict = frame_color_in
        frame_colors_out = await create_frame_colors(sessionmaker)
        result = await frame_colors_repository.update_one(id=-1, data=frame_color_dict)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(FrameColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, frame_color in zip(results, frame_colors_out):
            assert result == frame_color