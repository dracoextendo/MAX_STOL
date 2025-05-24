import asyncio
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.dao.base import BaseDAO
from src.models.orders import OrdersModel
from src.models.products import ProductsModel, DeskColors, FrameColors, Length, Depth, ProductDeskColor, ProductFrameColor, ProductLength, ProductDepth
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from src.database import async_session_maker
from src.models.users import UsersModel
from src.s3 import s3client
from src.schemas.products import SProductInfoOut, SProductOut
from src.schemas.settings import SDeskColorOut, SFrameColorOut, SLengthOut, SDepthOut


class ProductsDAO(BaseDAO):
    model = ProductsModel

    __mapper_args__ = {
        'passive_deletes': True  # Для корректной работы каскадного удаления
    }

    @staticmethod
    async def validate_parameters(params: list[int],
                                  param_name: str,
                                  model,
                                  session: AsyncSession):
        existing_params = await session.execute(
            select(model.id).where(model.id.in_(params))
        )
        existing_params = existing_params.scalars().all()
        for param_id in params:
            if param_id not in existing_params:
                raise HTTPException(status_code=404, detail=f"{param_name} id = {param_id} not found")

    @classmethod
    async def get_product(cls, product_id: int, active: bool):
        async with async_session_maker() as session:
            query = (
                select(ProductsModel)
                .options(
                    selectinload(ProductsModel.desk_colors),
                    selectinload(ProductsModel.frame_colors),
                    selectinload(ProductsModel.length),
                    selectinload(ProductsModel.depth)
                )
                .where(ProductsModel.id == product_id)
            )
            result = await session.execute(query)
            product = result.scalar_one_or_none()
            if not product:
                return None
            if not product.is_active:
                if active:
                    return None
            return SProductInfoOut(product=SProductOut(id = product.id,
                                                       name=product.name,
                                                       description = product.description,
                                                       price = product.price,
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
                                                      sort=length.sort) for length in product.length],
                                   depth=[SDepthOut(id=depth.id,
                                                 value=depth.value,
                                                 created_at=depth.created_at,
                                                 updated_at=depth.updated_at,
                                                    sort=depth.sort) for depth in product.depth], )

    @classmethod
    async def add_product(cls,
                          name: str,
                          description: str,
                          price: int,
                          first_image: UploadFile,
                          second_image: UploadFile,
                          third_image: UploadFile,
                          desk_colors: list[int],
                          frame_colors: list[int],
                          lengths: list[int],
                          depths: list[int],
                          sort: int | None,
                          is_active: bool | None,):
        async with async_session_maker() as validation_session:
            await cls.validate_parameters(desk_colors, 'Desk color', DeskColors, validation_session)
            await cls.validate_parameters(frame_colors, 'Frame color', FrameColors, validation_session)
            await cls.validate_parameters(lengths, 'Length', Length, validation_session)
            await cls.validate_parameters(depths, 'Depth', Depth, validation_session)

        async with async_session_maker() as session:
            async with session.begin():
                images_url = await asyncio.gather(
                    s3client.upload_to_s3(first_image),
                    s3client.upload_to_s3(second_image),
                    s3client.upload_to_s3(third_image),
                )
                product = ProductsModel(
                    name=name,
                    description=description,
                    price=price,
                    first_image=images_url[0],
                    second_image=images_url[1],
                    third_image=images_url[2],
                    sort=sort,
                    is_active=is_active
                )
                session.add(product)
                await session.flush()
                for desk_color_id in desk_colors:
                    session.add(ProductDeskColor(
                        product_id=product.id,
                        desk_color_id=desk_color_id
                    ))
                for frame_color_id in frame_colors:
                    session.add(ProductFrameColor(
                        product_id=product.id,
                        frame_color_id=frame_color_id
                    ))
                for length_id in lengths:
                    session.add(ProductLength(
                        product_id=product.id,
                        length_id=length_id
                    ))
                for depth_id in depths:
                    session.add(ProductDepth(
                        product_id=product.id,
                        depth_id=depth_id
                    ))
                return {"detail": f"Product id = {product.id} added"}

    @classmethod
    async def update_product(cls,
                             product_id: int,
                             name: str,
                             description: str,
                             price: int,
                             first_image: UploadFile,
                             second_image: UploadFile,
                             third_image: UploadFile,
                             desk_colors: list[int],
                             frame_colors: list[int],
                             lengths: list[int],
                             depths: list[int],
                             sort: int | None,
                             is_active: bool | None,):
        async with async_session_maker() as validation_session:
            await cls.validate_parameters(desk_colors, 'Desk color', DeskColors, validation_session)
            await cls.validate_parameters(frame_colors, 'Frame color', FrameColors, validation_session)
            await cls.validate_parameters(lengths, 'Length', Length, validation_session)
            await cls.validate_parameters(depths, 'Depth', Depth, validation_session)

        async with async_session_maker() as session:
            async with session.begin():
                product = await session.get(ProductsModel, product_id)
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product id = {product_id} not found")

                product.name = name
                product.description = description
                product.price = price
                product.sort = sort
                product.is_active = is_active

                await session.execute(delete(ProductDeskColor).where(ProductDeskColor.product_id == product_id))
                await session.execute(delete(ProductFrameColor).where(ProductFrameColor.product_id == product_id))
                await session.execute(delete(ProductLength).where(ProductLength.product_id == product_id))
                await session.execute(delete(ProductDepth).where(ProductDepth.product_id == product_id))

                for desk_color_id in desk_colors:
                    session.add(ProductDeskColor(
                        product_id=product_id,
                        desk_color_id=desk_color_id
                    ))
                for frame_color_id in frame_colors:
                    session.add(ProductFrameColor(
                        product_id=product_id,
                        frame_color_id=frame_color_id
                    ))
                for length_id in lengths:
                    session.add(ProductLength(
                        product_id=product_id,
                        length_id=length_id
                    ))
                for depth_id in depths:
                    session.add(ProductDepth(
                        product_id=product_id,
                        depth_id=depth_id
                    ))

                old_images = [product.first_image, product.second_image, product.third_image]
                new_images = [first_image, second_image, third_image]

                await asyncio.gather(*[s3client.delete_from_s3(img) for img in old_images])
                images_url = await asyncio.gather(*[s3client.upload_to_s3(img) for img in new_images])

                product.first_image = images_url[0]
                product.second_image = images_url[1]
                product.third_image = images_url[2]

                return {"detail": f"Product id = {product_id} updated"}

    @classmethod
    async def delete_product(cls, product_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                product = await session.get(ProductsModel, product_id)
                if not product:
                    return None
                files_to_delete = [
                    product.first_image,
                    product.second_image,
                    product.third_image
                ]
                await session.delete(product)
                await asyncio.gather(*[s3client.delete_from_s3(img) for img in files_to_delete])
        return {"detail": f"Product id = {product_id} deleted"}

class OrdersDAO(BaseDAO):
    model = OrdersModel

    @classmethod
    async def get_order(cls, order_id: int):
        async with async_session_maker() as session:
            return await session.get(OrdersModel, order_id)

    @classmethod
    async def add_order(cls, order: OrdersModel):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(order)
        return {"detail": "Order added"}

    @classmethod
    async def update_order(cls, order_id: int, order: OrdersModel):
        async with async_session_maker() as session:
            async with session.begin():
                current_order = await session.get(OrdersModel, order_id)
                if not current_order:
                    raise HTTPException(status_code=404, detail=f"Order id = {order_id} not found")
                order.id = order_id
                await session.merge(order)
        return {"detail": f"Order id = {order_id} updated"}

    @classmethod
    async def delete_order(cls, order_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                order = await session.get(OrdersModel, order_id)
                if not order:
                    raise HTTPException(status_code=404, detail=f"Order id = {order_id} not found")
                await session.delete(order)
        return {"detail": f"Order id = {order_id} deleted"}

class DeskColorDAO(BaseDAO):
    model = DeskColors

    @classmethod
    async def get_desk_color(cls, desk_color_id: int):
        async with async_session_maker() as session:
            return await session.get(DeskColors, desk_color_id)

    @classmethod
    async def add_desk_color(cls, desk_color: DeskColors):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(desk_color)
        return {"detail": "Desk color added"}

    @classmethod
    async def update_desk_color(cls, desk_color_id: int, desk_color: DeskColors):
        async with async_session_maker() as session:
            async with session.begin():
                current_desk_color = await session.get(DeskColors, desk_color_id)
                if not current_desk_color:
                    raise HTTPException(status_code=404, detail=f"Desk color id = {desk_color_id} not found")
                desk_color.id = desk_color_id
                await session.merge(desk_color)
        return {"detail": f"Desk color id = {desk_color_id} updated"}

    @classmethod
    async def delete_desk_color(cls, desk_color_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                desk_color = await session.get(DeskColors, desk_color_id)
                if not desk_color:
                    raise HTTPException(status_code=404, detail=f"Desk color id = {desk_color_id} not found")
                await session.delete(desk_color)
        return {"detail": f"Desk color id = {desk_color_id} deleted"}

class FrameColorDAO(BaseDAO):
    model = FrameColors

    @classmethod
    async def get_frame_color(cls, frame_color_id: int):
        async with async_session_maker() as session:
            return await session.get(FrameColors, frame_color_id)

    @classmethod
    async def add_frame_color(cls, frame_color: FrameColors):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(frame_color)
        return {"detail": "Frame color added"}

    @classmethod
    async def update_frame_color(cls, frame_color_id: int, frame_color: FrameColors):
        async with async_session_maker() as session:
            async with session.begin():
                current_frame_color = await session.get(FrameColors, frame_color_id)
                if not current_frame_color:
                    raise HTTPException(status_code=404, detail=f"Frame color id = {frame_color_id} not found")
                frame_color.id = frame_color_id
                await session.merge(frame_color)
        return {"detail": f"Frame color id = {frame_color_id} updated"}

    @classmethod
    async def delete_frame_color(cls, frame_color_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                frame_color = await session.get(FrameColors, frame_color_id)
                if not frame_color:
                    raise HTTPException(status_code=404, detail=f"Frame color id = {frame_color_id} not found")
                await session.delete(frame_color)
        return {"detail": f"Frame color id = {frame_color_id} deleted"}

class DepthDAO(BaseDAO):
    model = Depth

    @classmethod
    async def get_depth(cls, depth_id: int):
        async with async_session_maker() as session:
            return await session.get(Depth, depth_id)

    @classmethod
    async def add_depth(cls, depth: Depth):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(depth)
        return {"detail": "Depth added"}

    @classmethod
    async def update_depth(cls, depth_id: int, depth: Depth):
        async with async_session_maker() as session:
            async with session.begin():
                current_depth = await session.get(Depth, depth_id)
                if not current_depth:
                    raise HTTPException(status_code=404, detail=f"Depth id = {depth_id} not found")
                depth.id = depth_id
                await session.merge(depth)
        return {"detail": f"Depth id = {depth_id} updated"}

    @classmethod
    async def delete_depth(cls, depth_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                depth = await session.get(Depth, depth_id)
                if not depth:
                    raise HTTPException(status_code=404, detail=f"Depth id = {depth_id} not found")
                await session.delete(depth)
        return {"detail": f"Depth id = {depth_id} deleted"}

class LengthDAO(BaseDAO):
    model = Length

    @classmethod
    async def get_length(cls, length_id: int):
        async with async_session_maker() as session:
            return await session.get(Length, length_id)

    @classmethod
    async def add_length(cls, length: Length):
        async with async_session_maker() as session:
            async with session.begin():
                session.add(length)
        return {"detail": "Length added"}

    @classmethod
    async def update_length(cls, length_id: int, length: Length):
        async with async_session_maker() as session:
            async with session.begin():
                current_length = await session.get(Length, length_id)
                if not current_length:
                    raise HTTPException(status_code=404, detail=f"Length id = {length_id} not found")
                length.id = length_id
                await session.merge(length)
        return {"detail": f"Length id = {length_id} updated"}

    @classmethod
    async def delete_length(cls, length_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                length = await session.get(Length, length_id)
                if not length:
                    raise HTTPException(status_code=404, detail=f"Length id = {length_id} not found")
                await session.delete(length)
        return {"detail": f"Length id = {length_id} deleted"}

class UsersDAO(BaseDAO):
    model = UsersModel

    @classmethod
    async def get_user_by_username(cls, username: str):
        async with async_session_maker() as session:
            query = select(UsersModel).where(
                UsersModel.username == username
            )
            result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_user_by_id(cls, user_id: int):
        async with async_session_maker() as session:
            return await session.get(UsersModel, user_id)