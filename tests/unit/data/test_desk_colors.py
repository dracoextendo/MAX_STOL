import pytest
from sqlalchemy import select
from src.models.products import DeskColors
from src.schemas.desk_settings import SDeskColorIn, SDeskColorOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError

async def create_desk_colors(sessionmaker) -> list[SDeskColorOut]:
    test_desk_colors_models = [DeskColors(id=1,
                                          name="name_1",
                                          sort=100
                                      ),
                               DeskColors(id=2,
                                          name="name_2",
                                          sort=200
                                      ),
                               DeskColors(id=3,
                                          name="name_3",
                                          sort=300
                                          ),
                          ]
    async with sessionmaker() as session:
        for desk_color in test_desk_colors_models:
            session.add(desk_color)
        await session.commit()
    test_desk_colors_schemas = [model.to_read_model() for model in test_desk_colors_models]
    return test_desk_colors_schemas

@pytest.fixture
def desk_color_in() -> dict:
    desk_color_in = SDeskColorIn(name="name_1",
                            sort=100
                            )
    return desk_color_in.model_dump()


class TestDeskColorsGetOne:
    @pytest.mark.asyncio
    async def test_get_one(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.get_one(id=1)
        assert result is not None
        assert SDeskColorOut.model_validate(result)
        assert result == desk_colors_out[0]

    @pytest.mark.asyncio
    async def test_get_one_not_existing(self, desk_colors_repository):
        result = await desk_colors_repository.get_one(id=-1)
        assert result is None

class TestDeskColorsGetAll:
    @pytest.mark.asyncio
    async def test_get_all_empty(self, desk_colors_repository):
        results = await desk_colors_repository.get_all()
        assert results == []

    @pytest.mark.asyncio
    async def test_get_all_no_empty(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        results = await desk_colors_repository.get_all()
        assert len(results) == 3
        for result, desk_color in zip(results, desk_colors_out):
            assert result == desk_color

    @pytest.mark.asyncio
    async def test_get_all_filtered(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        results = await desk_colors_repository.get_all(filter_by={'name': "name_1"})
        assert len(results) == 1
        assert results[0] == desk_colors_out[0]

    @pytest.mark.asyncio
    async def test_get_all_ordered(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        results = await desk_colors_repository.get_all(order_by='-id')
        assert len(results) == 3
        for result, desk_color in zip(results, reversed(desk_colors_out)):
            assert result == desk_color

    @pytest.mark.asyncio
    async def test_get_all_ordered_by_many(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        results = await desk_colors_repository.get_all(order_by=['-id', 'name'])
        assert len(results) == 3
        for result, desk_color in zip(results, reversed(desk_colors_out)):
            assert result == desk_color

    @pytest.mark.asyncio
    async def test_get_all_incorrect_filtered(self, desk_colors_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await desk_colors_repository.get_all(filter_by={'user': "username_1"})
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "desk_colors" has no property "user"' in str(e.value)

    @pytest.mark.asyncio
    async def test_get_all_incorrect_ordered(self, desk_colors_repository, sessionmaker):
        with pytest.raises(Exception) as e:
            await desk_colors_repository.get_all(order_by='-qwe')
        assert e.type == InvalidRequestError
        assert 'Entity namespace for "desk_colors" has no property "qwe"' in str(e.value)

class TestDeskColorsAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, desk_colors_repository, sessionmaker, desk_color_in):
        desk_color_dict = desk_color_in
        result = await desk_colors_repository.add_one(desk_color_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(DeskColors, 1)
        assert SDeskColorOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, desk_colors_repository, desk_color_in):
        desk_color_dict = desk_color_in
        first_result = await desk_colors_repository.add_one(desk_color_dict)
        second_result = await desk_colors_repository.add_one(desk_color_dict)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_name(self, desk_colors_repository, desk_color_in):
        desk_color_dict = desk_color_in
        desk_color_dict.pop('name')
        with pytest.raises(Exception) as e:
            await desk_colors_repository.add_one(desk_color_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: desk_colors.name" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_sort(self, desk_colors_repository, desk_color_in):
        desk_color_dict = desk_color_in
        desk_color_dict.pop('sort')
        result = await desk_colors_repository.add_one(desk_color_dict)
        assert result is not None
        assert result == 1

    @pytest.mark.asyncio
    async def test_add_one_no_all(self, desk_colors_repository):
        desk_color_dict = {}
        with pytest.raises(Exception) as e:
            await desk_colors_repository.add_one(desk_color_dict)
        assert e.type == IntegrityError

class TestDeskColorsDeleteOne:
    @pytest.mark.asyncio
    async def test_delete_one(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.delete_one(id = desk_colors_out[0].id)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            stmt = select(DeskColors)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 2
        assert desk_colors_out[0] not in orders
        for desk_color, order_out in zip(orders, desk_colors_out[1:]):
            assert desk_color == order_out

    @pytest.mark.asyncio
    async def test_delete_one_not_existing(self, desk_colors_repository, sessionmaker):
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.delete_one(id=-1)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(DeskColors)
            res_all = await session.execute(stmt)
        orders = [row[0].to_read_model() for row in res_all.all()]
        assert len(orders) == 3
        assert desk_colors_out[0] in orders
        for desk_color, order_out in zip(orders, desk_colors_out):
            assert desk_color == order_out

class TestDeskColorsUpdateOne:
    @pytest.mark.asyncio
    async def test_update_one_full(self, desk_colors_repository, sessionmaker, desk_color_in):
        desk_color_dict = desk_color_in
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.update_one(id = 3, data=desk_color_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            res_one = await session.get(DeskColors, 3)
        desk_colors_out[2] = res_one.to_read_model()
        async with sessionmaker() as session:
            stmt = select(DeskColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, desk_color in zip(results, desk_colors_out):
            assert result == desk_color

    @pytest.mark.asyncio
    async def test_update_one_empty(self, desk_colors_repository, sessionmaker):
        desk_color_dict = {}
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.update_one(id=3, data=desk_color_dict)
        assert result is not None
        assert result == 3
        async with sessionmaker() as session:
            stmt = select(DeskColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, desk_color in zip(results, desk_colors_out):
            assert result == desk_color

    @pytest.mark.asyncio
    async def test_update_one_not_existing(self, desk_colors_repository, sessionmaker, desk_color_in):
        desk_color_dict = desk_color_in
        desk_colors_out = await create_desk_colors(sessionmaker)
        result = await desk_colors_repository.update_one(id=-1, data=desk_color_dict)
        assert result is None
        async with sessionmaker() as session:
            stmt = select(DeskColors)
            res_all = await session.execute(stmt)
        results = [row[0].to_read_model() for row in res_all.all()]
        for result, desk_color in zip(results, desk_colors_out):
            assert result == desk_color