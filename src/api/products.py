import asyncio
from typing import Annotated

from fastapi import APIRouter, Form, UploadFile

from src.dao.dao import ProductsDAO
from src.models.products import ProductsModel
from src.schemas.products import SGetProduct
from src.s3 import s3client

router = APIRouter()

@router.get("/get_products", response_model=list[SGetProduct])
async def get_products():
    return await ProductsDAO().find_all()

@router.get("/product/{id}")
async def get_product(id: int):
    return await ProductsDAO.get_product(id)

@router.post("/upload_product")
async def upload_product(
        name: Annotated[str, Form()],
        description: Annotated[str, Form()],
        price: Annotated[int, Form()],
        first_image: UploadFile,
        second_image: UploadFile,
        third_image: UploadFile,
):
    image_urls = await asyncio.gather(
        s3client.upload_to_s3(first_image),
        s3client.upload_to_s3(second_image),
        s3client.upload_to_s3(third_image)
    )
    new_product = ProductsModel(
        name=name,
        description=description,
        price=price,
        first_image=image_urls[0],
        second_image=image_urls[1],
        third_image=image_urls[2],
    )
    return await ProductsDAO.add(new_product)
