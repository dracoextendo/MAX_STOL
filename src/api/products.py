from typing import Annotated
from fastapi import APIRouter, Form, UploadFile, status, HTTPException
from fastapi.params import Depends

from src.api.responses import NOT_FOUND, UNAUTHORIZED, FORBIDDEN
from src.dao.dao import ProductsDAO
from src.schemas.base import SStatusOut
from src.schemas.products import SProductInfoOut, SProductOut, SProductIn
from src.api.dependencies import access_token_validation

router = APIRouter(tags=['Продукты'], prefix='/products')

@router.get("",
            response_model=list[SProductOut],
            summary="Получить все продукты")
async def get_all_products():
    return await ProductsDAO().find_all()

@router.get("/{id}",
            responses ={**NOT_FOUND},
            response_model=SProductInfoOut,
            summary="Получить информацию о продукте по id")
async def get_product_by_id(id: int):
    result = await ProductsDAO.get_product(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.delete("/{id}",
               dependencies=[Depends(access_token_validation)],
               responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить продукт")
async def delete_product(id: int):
    result = await ProductsDAO.delete_product(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.put("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить продукт (в Swagger можно добавить только по одной характеристике)")
async def update_product(id: int, product_data: SProductIn = Depends(SProductIn.as_form)):
    return await ProductsDAO.update_product(product_id=id,
                                            name=product_data.name,
                                            description=product_data.description,
                                            price=product_data.price,
                                            first_image=product_data.first_image,
                                            second_image=product_data.second_image,
                                            third_image=product_data.third_image,
                                            desk_colors=product_data.desk_colors,
                                            frame_colors=product_data.frame_colors,
                                            lengths=product_data.lengths,
                                            depths=product_data.depths,)

@router.post("/add",
             dependencies=[Depends(access_token_validation)],
             responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
             response_model=SStatusOut,
             summary="Добавить продукт (в Swagger можно добавить только по одной характеристике, добавление нескольких характеристик через /test-form)",
             status_code=status.HTTP_201_CREATED)
async def upload_product(product_data: SProductIn = Depends(SProductIn.as_form)):
    return await ProductsDAO.add_product(name=product_data.name,
                                         description=product_data.description,
                                         price=product_data.price,
                                         first_image=product_data.first_image,
                                         second_image=product_data.second_image,
                                         third_image=product_data.third_image,
                                         desk_colors=product_data.desk_colors,
                                         frame_colors=product_data.frame_colors,
                                         lengths=product_data.lengths,
                                         depths=product_data.depths)