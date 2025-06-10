import pytest
from fastapi import File
from sqlalchemy import select
from src.models.products import ProductsModel
from src.schemas.products import SProductIn, SProductOut, SProductInfoOut
from sqlalchemy.exc import IntegrityError, InvalidRequestError

@pytest.fixture
def product_in() -> dict:
    product_in = {
        'name': "Test Product",
        'description': "Test Description",
        'price': 1000,
        'first_image': "https://test.ru/image1",
        'second_image': "https://test.ru/image2",
        'third_image': "https://test.ru/image3",
        'desk_colors': [1],
        'frame_colors': [1],
        'lengths': [1],
        'depths': [1],
        'sort': 300,
        'is_active': True,
    }
    return product_in

class TestProductsAddOne:
    @pytest.mark.asyncio
    async def test_add_one(self, products_repository, sessionmaker, product_in):
        product_dict = product_in.copy()
        result = await products_repository.add_one(product_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(ProductsModel, 1)
        assert SProductOut.model_validate(added_value.to_read_model())

    @pytest.mark.asyncio
    async def test_add_one_twice(self, products_repository, product_in):
        product_dict1 = product_in.copy()
        product_dict2 = product_in.copy()
        first_result = await products_repository.add_one(product_dict1)
        second_result = await products_repository.add_one(product_dict2)
        assert first_result is not None
        assert second_result is not None
        assert first_result == 1
        assert second_result == 2

    @pytest.mark.asyncio
    async def test_add_one_no_sort(self, products_repository, sessionmaker, product_in):
        product_dict = product_in.copy()
        product_dict.pop('sort')
        result = await products_repository.add_one(product_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(ProductsModel, 1)
        assert SProductOut.model_validate(added_value.to_read_model())
        assert added_value.sort == 500

    @pytest.mark.asyncio
    async def test_add_one_no_is_active(self, products_repository, sessionmaker, product_in):
        product_dict = product_in.copy()
        product_dict.pop('is_active')
        result = await products_repository.add_one(product_dict)
        assert result is not None
        assert result == 1
        async with sessionmaker() as session:
            added_value = await session.get(ProductsModel, 1)
        assert SProductOut.model_validate(added_value.to_read_model())
        assert added_value.is_active == True

    @pytest.mark.asyncio
    async def test_add_one_no_name(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('name')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.name" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_description(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('description')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.description" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_price(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('price')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.price" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_first_image(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('first_image')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.first_image" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_second_image(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('second_image')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.second_image" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_third_image(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('third_image')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError
        assert "NOT NULL constraint failed: products.third_image" in str(e.value)

    @pytest.mark.asyncio
    async def test_add_one_no_desk_colors(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('desk_colors')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError

    @pytest.mark.asyncio
    async def test_add_one_no_frame_colors(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('frame_colors')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError

    @pytest.mark.asyncio
    async def test_add_one_no_lengths(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('lengths')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError

    @pytest.mark.asyncio
    async def test_add_one_no_depths(self, products_repository, product_in):
        product_dict = product_in.copy()
        product_dict.pop('depths')
        with pytest.raises(Exception) as e:
            await products_repository.add_one(product_dict)
        assert e.type == IntegrityError