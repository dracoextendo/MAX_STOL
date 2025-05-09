import asyncio
from fastapi import UploadFile, HTTPException
from src.dao.base import BaseDAO
from src.models.products import ProductsModel, DeskColors, FrameColors, Length, Depth, ProductDeskColor, \
    ProductFrameColor, ProductLength, ProductDepth
from sqlalchemy.orm import selectinload
from sqlalchemy import select, delete
from src.database import async_session_maker
from src.s3 import S3Client

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
