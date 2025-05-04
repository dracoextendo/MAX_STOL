from typing import Annotated

from fastapi import APIRouter, Form, UploadFile, File

from src.dao.dao import ProductsDAO
from src.models.products import ProductsModel
from src.schemas.products import SGetProduct

router = APIRouter()

@router.get("/get_products", response_model=list[SGetProduct])
async def get_products():
    return await ProductsDAO().find_all()

@router.post("/upload_product")
async def upload_product(
        name: Annotated[str, Form()],
        description: Annotated[str, Form()],
        price: Annotated[float, Form()],
        first_image: UploadFile,
        second_image: UploadFile,
        third_image: UploadFile,
):
    new_product = ProductsModel(
        name=name,
        description=description,
        price=price,
        first_image=first_image.filename,
        second_image=second_image.filename,
        third_image=third_image.filename,
    )

    return await ProductsDAO.add(new_product)
