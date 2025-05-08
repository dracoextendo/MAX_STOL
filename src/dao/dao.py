from src.dao.base import BaseDAO
from src.models.products import ProductsModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from src.database import async_session_maker

class ProductsDAO(BaseDAO):
    model = ProductsModel

    @classmethod
    async def get_product(cls, product_id: int):
        async with async_session_maker() as session:
            stmt = (
                select(ProductsModel)
                .options(
                    selectinload(ProductsModel.desk_colors),
                    selectinload(ProductsModel.frame_colors),
                    selectinload(ProductsModel.length),
                    selectinload(ProductsModel.depth)
                )
                .where(ProductsModel.id == product_id)
            )
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if not product:
                return None

            return {
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "first_image": product.first_image,
                    "second_image": product.second_image,
                    "third_image": product.third_image,
                },
                "desk_colors": [color.name for color in product.desk_colors],
                "frame_colors": [color.name for color in product.frame_colors],
                "length": [length.value for length in product.length],
                "depth": [depth.value for depth in product.depth]
            }