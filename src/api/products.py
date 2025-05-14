from typing import Annotated
from authx.exceptions import MissingTokenError
from fastapi import APIRouter, Form, UploadFile, status, HTTPException, Request
from fastapi.params import Depends

from src.dao.dao import ProductsDAO
from src.schemas.base import SBaseStatus
from src.schemas.products import SGetProductInfo, SGetProduct
from src.s3 import s3client
from src.security import security

router = APIRouter(tags=['Продукты'], prefix='/product')

@router.get("/get_all", response_model=list[SGetProduct], summary="Получить все продукты")
async def get_all_products():
    return await ProductsDAO().find_all()

@router.get("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SGetProductInfo, summary="Получить информацию о продукте по id")
async def get_product_by_id(id: int):
    result = await ProductsDAO.get_product(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.post("/upload", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Добавить продукт (не работает добавление нескольких характеристик через бэк, надо тестить на фронте)", status_code=status.HTTP_201_CREATED)
async def upload_product(name: Annotated[str, Form()], description: Annotated[str, Form()], price: Annotated[int, Form()], first_image: UploadFile, second_image: UploadFile, third_image: UploadFile, desk_colors: Annotated[list[int], Form()],
    frame_colors: Annotated[list[int], Form()],
    lengths: Annotated[list[int], Form()],
    depths: Annotated[list[int], Form()]):
    return await ProductsDAO.add_product(name, description, price, first_image, second_image, third_image, desk_colors, frame_colors, lengths, depths, s3client)

@router.delete("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Удалить продукт")
async def delete_product(id: int):
    result = await ProductsDAO.delete_product(id, s3client)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result