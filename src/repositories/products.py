from typing import override
from sqlalchemy import insert, select, delete, update
from sqlalchemy.orm import selectinload
from src.models.products import ProductsModel, ProductDeskColor, ProductFrameColor, ProductLength, ProductDepth
from src.schemas.products import SProductInfoOut, SProductOut
from src.schemas.desk_settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut
from src.utils.repository import SQLAlchemyRepository


class ProductsRepository(SQLAlchemyRepository):
    model = ProductsModel

    __mapper_args__ = {
        'passive_deletes': True  # Для корректной работы каскадного удаления
    }

    @override
    async def add_one(self, data: dict) -> int:
        desk_colors = data.pop('desk_colors', [])
        frame_colors = data.pop('frame_colors', [])
        lengths = data.pop('lengths', [])
        depths = data.pop('depths', [])

        async with self.session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            product_id = res.scalar_one()

            await session.execute(insert(ProductDeskColor), [{"product_id": product_id, "desk_color_id": c} for c in desk_colors])
            await session.execute(insert(ProductFrameColor), [{"product_id": product_id, "frame_color_id": c} for c in frame_colors])
            await session.execute(insert(ProductLength), [{"product_id": product_id, "length_id": v} for v in lengths])
            await session.execute(insert(ProductDepth), [{"product_id": product_id, "depth_id": v} for v in depths])

            await session.commit()
            return product_id

    @override
    async def delete_one(self, id: int) -> list[str] | None:
        async with self.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            product = res.scalar_one_or_none()
            if not product:
                return None
            stmt = delete(self.model).where(self.model.id == id)
            await session.execute(stmt)
            await session.commit()
            return [product.first_image, product.second_image, product.third_image]

    @override
    async def update_one(self, id: int, data: dict) -> int | None:
        desk_colors = data.pop('desk_colors', [])
        frame_colors = data.pop('frame_colors', [])
        lengths = data.pop('lengths', [])
        depths = data.pop('depths', [])

        async with self.session_factory() as session:
            stmt = select(self.model).where(self.model.id == id)
            res = await session.execute(stmt)
            product = res.scalar_one_or_none()
            if not product:
                return None
            stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            product_id = res.scalar_one()
            await session.execute(delete(ProductDeskColor).where(ProductDeskColor.product_id == id))
            await session.execute(delete(ProductFrameColor).where(ProductFrameColor.product_id == id))
            await session.execute(delete(ProductLength).where(ProductLength.product_id == id))
            await session.execute(delete(ProductDepth).where(ProductDepth.product_id == id))
            await session.execute(insert(ProductDeskColor),[{"product_id": id, "desk_color_id": c} for c in desk_colors])
            await session.execute(insert(ProductFrameColor),[{"product_id": id, "frame_color_id": c} for c in frame_colors])
            await session.execute(insert(ProductLength), [{"product_id": id, "length_id": v} for v in lengths])
            await session.execute(insert(ProductDepth), [{"product_id": id, "depth_id": v} for v in depths])
            await session.commit()
            return product_id


    @override
    async def get_info(self, id: int) -> SProductInfoOut | None:
        async with self.session_factory() as session:
            stmt = select(self.model).options(
                    selectinload(self.model.desk_colors),
                    selectinload(self.model.frame_colors),
                    selectinload(self.model.lengths),
                    selectinload(self.model.depths)
                ).where(self.model.id == id)
            res = await session.execute(stmt)
            product = res.scalar_one_or_none()
            if not product:
                return None
            return SProductInfoOut(product=SProductOut(id=product.id,
                                                       name=product.name,
                                                       description=product.description,
                                                       price=product.price,
                                                       first_image=product.first_image,
                                                       second_image=product.second_image,
                                                       third_image=product.third_image,
                                                       created_at=product.created_at,
                                                       updated_at=product.updated_at,
                                                       sort=product.sort,
                                                       is_active=product.is_active,
                                                       ),
                                   desk_colors=[SDeskColorOut(id=d_color.id,
                                                              name=d_color.name,
                                                              created_at=d_color.created_at,
                                                              updated_at=d_color.updated_at,
                                                              sort=d_color.sort) for d_color in product.desk_colors],
                                   frame_colors=[SFrameColorOut(id=f_color.id,
                                                                name=f_color.name,
                                                                created_at=f_color.created_at,
                                                                updated_at=f_color.updated_at,
                                                                sort=f_color.sort) for f_color in product.frame_colors],
                                   length=[SLengthOut(id=length.id,
                                                      value=length.value,
                                                      created_at=length.created_at,
                                                      updated_at=length.updated_at,
                                                      sort=length.sort) for length in product.lengths],
                                   depth=[SDepthOut(id=depth.id,
                                                    value=depth.value,
                                                    created_at=depth.created_at,
                                                    updated_at=depth.updated_at,
                                                    sort=depth.sort) for depth in product.depths], )
