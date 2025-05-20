import asyncio
from fastapi import UploadFile, HTTPException
from src.dao.base import BaseDAO
from src.models.orders import OrdersModel
from src.models.products import ProductsModel, DeskColors, FrameColors, Length, Depth, ProductDeskColor, ProductFrameColor, ProductLength, ProductDepth
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from src.database import async_session_maker
from src.models.users import UsersModel
from src.s3 import S3Client


class ProductsDAO(BaseDAO):
    model = ProductsModel

    @classmethod
    async def get_product(cls, product_id: int):
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
                "desk_colors": [{"id": color.id,"color": color.name} for color in product.desk_colors],
                "frame_colors": [{"id": color.id,"color": color.name} for color in product.frame_colors],
                "length": [{"id": length.id, "value": length.value} for length in product.length],
                "depth": [{"id": depth.id, "value": depth.value} for depth in product.depth]
            }

    @classmethod
    async def add_product(cls, name: str, description: str, price: int, first_image: UploadFile,
                          second_image: UploadFile, third_image: UploadFile, desk_colors: list[int], frame_colors: list[int], lengths: list[int], depths: list[int], s3client: S3Client):
        images_url = await asyncio.gather(
            s3client.upload_to_s3(first_image),
            s3client.upload_to_s3(second_image),
            s3client.upload_to_s3(third_image),
        )

        async with async_session_maker() as session:
            async with session.begin():
                # 1. Создаём продукт
                product = ProductsModel(
                    name=name,
                    description=description,
                    price=price,
                    first_image=images_url[0],
                    second_image=images_url[1],
                    third_image=images_url[2],
                )
                session.add(product)
                await session.flush()  # Получаем ID

                # 2. Проверяем и добавляем связи
                if desk_colors:
                    # Проверяем существование цветов столешницы
                    existing_desk_colors = await session.execute(
                        select(DeskColors.id).where(DeskColors.id.in_(desk_colors))
                    )
                    existing_desk_colors = existing_desk_colors.scalars().all()

                    for color_id in desk_colors:
                        if color_id not in existing_desk_colors:
                            async with s3client.get_client() as s3_client:
                                delete_tasks = []
                                for file_url in images_url:
                                    if file_url:  # Проверяем, что URL существует
                                        file_name = file_url.split('/')[-1]  # Извлекаем имя файла из URL
                                        delete_tasks.append(
                                            s3_client.delete_object(
                                                Bucket=s3client.bucket_name,
                                                Key=file_name
                                            )
                                        )
                                if delete_tasks: await asyncio.gather(*delete_tasks)
                            raise HTTPException(status_code=404, detail=f"Desk color id = {color_id} not found")
                        session.add(ProductDeskColor(
                            product_id=product.id,
                            desk_color_id=color_id
                        ))

                if frame_colors:
                    # Проверяем существование цветов каркаса
                    existing_frame_colors = await session.execute(
                        select(FrameColors.id).where(FrameColors.id.in_(frame_colors))
                    )
                    existing_frame_colors = existing_frame_colors.scalars().all()

                    for color_id in frame_colors:
                        if color_id not in existing_frame_colors:
                            async with s3client.get_client() as s3_client:
                                delete_tasks = []
                                for file_url in images_url:
                                    if file_url:  # Проверяем, что URL существует
                                        file_name = file_url.split('/')[-1]  # Извлекаем имя файла из URL
                                        delete_tasks.append(
                                            s3_client.delete_object(
                                                Bucket=s3client.bucket_name,
                                                Key=file_name
                                            )
                                        )
                                if delete_tasks: await asyncio.gather(*delete_tasks)
                            raise HTTPException(status_code=404, detail=f"Frame color id = {color_id} not found")
                        session.add(ProductFrameColor(
                            product_id=product.id,
                            frame_color_id=color_id
                        ))

                if lengths:
                    # Проверяем существование длин
                    existing_lengths = await session.execute(
                        select(Length.id).where(Length.id.in_(lengths))
                    )
                    existing_lengths = existing_lengths.scalars().all()

                    for length_id in lengths:
                        if length_id not in existing_lengths:
                            async with s3client.get_client() as s3_client:
                                delete_tasks = []
                                for file_url in images_url:
                                    if file_url:  # Проверяем, что URL существует
                                        file_name = file_url.split('/')[-1]  # Извлекаем имя файла из URL
                                        delete_tasks.append(
                                            s3_client.delete_object(
                                                Bucket=s3client.bucket_name,
                                                Key=file_name
                                            )
                                        )
                                if delete_tasks: await asyncio.gather(*delete_tasks)
                            raise HTTPException(status_code=404, detail=f"Length id = {length_id} not found")
                        session.add(ProductLength(
                            product_id=product.id,
                            length_id=length_id
                        ))

                if depths:
                    # Проверяем существование глубин
                    existing_depths = await session.execute(
                        select(Depth.id).where(Depth.id.in_(depths))
                    )
                    existing_depths = existing_depths.scalars().all()

                    for depth_id in depths:
                        if depth_id not in existing_depths:
                            async with s3client.get_client() as s3_client:
                                delete_tasks = []
                                for file_url in images_url:
                                    if file_url:  # Проверяем, что URL существует
                                        file_name = file_url.split('/')[-1]  # Извлекаем имя файла из URL
                                        delete_tasks.append(
                                            s3_client.delete_object(
                                                Bucket=s3client.bucket_name,
                                                Key=file_name
                                            )
                                        )
                                if delete_tasks: await asyncio.gather(*delete_tasks)
                            raise HTTPException(status_code=404, detail=f"Depth id = {depth_id} not found")
                        session.add(ProductDepth(
                            product_id=product.id,
                            depth_id=depth_id
                        ))

        return {"status": "Product added"}



    __mapper_args__ = {
        'passive_deletes': True  # Для корректной работы каскадного удаления
    }

    @classmethod
    async def delete_product(cls, product_id: int, s3client: S3Client):
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
            async with s3client.get_client() as s3_client:
                delete_tasks = []
                for file_url in files_to_delete:
                    if file_url:  # Проверяем, что URL существует
                        file_name = file_url.split('/')[-1]  # Извлекаем имя файла из URL
                        delete_tasks.append(
                            s3_client.delete_object(
                                Bucket=s3client.bucket_name,
                                Key=file_name
                            )
                        )
                if delete_tasks: await asyncio.gather(*delete_tasks)
        return {"status": "Product deleted"}

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
        return {"status": "Order added"}

    @classmethod
    async def update_order(cls, order_id: int, order: OrdersModel):
        async with async_session_maker() as session:
            async with session.begin():
                current_order = await session.get(OrdersModel, order_id)
                if not current_order:
                    raise HTTPException(status_code=404, detail=f"Order id = {order_id} not found")
                order.id = order_id
                await session.merge(order)
        return {"status": "Order updated"}

    @classmethod
    async def delete_order(cls, order_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                order = await session.get(OrdersModel, order_id)
                if not order:
                    raise HTTPException(status_code=404, detail=f"Order id = {order_id} not found")
                await session.delete(order)
        return {"status": "Order deleted"}

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
        return {"status": "Desk color added"}

    @classmethod
    async def update_desk_color(cls, desk_color_id: int, desk_color: DeskColors):
        async with async_session_maker() as session:
            async with session.begin():
                current_desk_color = await session.get(DeskColors, desk_color_id)
                if not current_desk_color:
                    raise HTTPException(status_code=404, detail=f"Desk color id = {desk_color_id} not found")
                desk_color.id = desk_color_id
                await session.merge(desk_color)
        return {"status": "Desk color updated"}

    @classmethod
    async def delete_desk_color(cls, desk_color_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                desk_color = await session.get(DeskColors, desk_color_id)
                if not desk_color:
                    raise HTTPException(status_code=404, detail=f"Desk color id = {desk_color_id} not found")
                await session.delete(desk_color)
        return {"status": "Desk color deleted"}

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
        return {"status": "Frame color added"}

    @classmethod
    async def update_frame_color(cls, frame_color_id: int, frame_color: FrameColors):
        async with async_session_maker() as session:
            async with session.begin():
                current_frame_color = await session.get(FrameColors, frame_color_id)
                if not current_frame_color:
                    raise HTTPException(status_code=404, detail=f"Frame color id = {frame_color_id} not found")
                frame_color.id = frame_color_id
                await session.merge(frame_color)
        return {"status": "Frame color updated"}

    @classmethod
    async def delete_frame_color(cls, frame_color_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                frame_color = await session.get(FrameColors, frame_color_id)
                if not frame_color:
                    raise HTTPException(status_code=404, detail=f"Frame color id = {frame_color_id} not found")
                await session.delete(frame_color)
        return {"status": "Frame color deleted"}

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
        return {"status": "Depth added"}

    @classmethod
    async def update_depth(cls, depth_id: int, depth: Depth):
        async with async_session_maker() as session:
            async with session.begin():
                current_depth = await session.get(Depth, depth_id)
                if not current_depth:
                    raise HTTPException(status_code=404, detail=f"Depth id = {depth_id} not found")
                depth.id = depth_id
                await session.merge(depth)
        return {"status": "Depth updated"}

    @classmethod
    async def delete_depth(cls, depth_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                depth = await session.get(Depth, depth_id)
                if not depth:
                    raise HTTPException(status_code=404, detail=f"Depth id = {depth_id} not found")
                await session.delete(depth)
        return {"status": "Depth deleted"}

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
        return {"status": "Length added"}

    @classmethod
    async def update_length(cls, length_id: int, length: Length):
        async with async_session_maker() as session:
            async with session.begin():
                current_length = await session.get(Length, length_id)
                if not current_length:
                    raise HTTPException(status_code=404, detail=f"Length id = {length_id} not found")
                length.id = length_id
                await session.merge(length)
        return {"status": "Length updated"}

    @classmethod
    async def delete_length(cls, length_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                length = await session.get(Length, length_id)
                if not length:
                    raise HTTPException(status_code=404, detail=f"Length id = {length_id} not found")
                await session.delete(length)
        return {"status": "Length deleted"}

class UsersDAO(BaseDAO):
    model = UsersModel

    @classmethod
    async def get_user(cls, username: str):
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