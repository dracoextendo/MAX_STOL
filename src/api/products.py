import asyncio
from fastapi import APIRouter, status, HTTPException, Request, Response
from fastapi.params import Depends
from src.utils.responses import NOT_FOUND, UNAUTHORIZED
from src.schemas.base import SStatusOut
from src.schemas.products import SProductInfoOut, SProductOut, SProductIn
from src.api.dependencies import s3_service, product_service, desk_color_service, \
    frame_color_service, length_service, depth_service, auth_service
from src.services.auth import AuthService
from src.services.products import ProductsService
from src.services.s3 import S3Service
from src.services.desk_settings import SettingsService
from src.utils.config import SECURE_COOKIE

router = APIRouter(tags=['Продукты'], prefix='/products')

@router.get("", response_model=list[SProductOut], summary="Получить все активные продукты")
async def get_all_active_products(product_service: ProductsService = Depends(product_service)):
    products = await product_service.get_all_products(filter_by={'is_active': True}, order_by = ["sort", "id"])
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    return products

@router.get("/{id}", responses ={**NOT_FOUND}, response_model=SProductInfoOut, summary="Получить информацию о продукте")
async def get_product_info(id: int, product_service: ProductsService = Depends(product_service)):
    product = await product_service.get_info(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{id}",
               responses ={**UNAUTHORIZED, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить продукт")
async def delete_product(request: Request,
                         response: Response,
                         id: int,
                         product_service: ProductsService = Depends(product_service),
                         image_service: S3Service = Depends(s3_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    files_to_delete = await product_service.delete_product(id)
    if not files_to_delete:
        raise HTTPException(status_code=404, detail="Product not found")
    await asyncio.gather(*[image_service.delete_file(url) for url in files_to_delete])
    return SStatusOut(detail=f"product id = {id} deleted")

@router.put("/{id}",
            responses ={**UNAUTHORIZED, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить продукт (в Swagger можно добавить только по одной характеристике)")
async def update_product(request: Request,
                         response: Response,
                         id: int,
                         product_data: SProductIn = Depends(SProductIn.as_form),
                         product_service: ProductsService = Depends(product_service),
                         image_service: S3Service = Depends(s3_service),
                         desk_color_service: SettingsService = Depends(desk_color_service),
                         frame_color_service: SettingsService = Depends(frame_color_service),
                         length_service: SettingsService = Depends(length_service),
                         depth_service: SettingsService = Depends(depth_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    product = await product_service.get_product(id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not await desk_color_service.validate_parameters(product_data.desk_colors):
        raise HTTPException(status_code=400, detail="Invalid desk colors")
    if not await frame_color_service.validate_parameters(product_data.frame_colors):
        raise HTTPException(status_code=400, detail="Invalid frame colors")
    if not await length_service.validate_parameters(product_data.lengths):
        raise HTTPException(status_code=400, detail="Invalid lengths")
    if not await depth_service.validate_parameters(product_data.depths):
        raise HTTPException(status_code=400, detail="Invalid depths")

    image_urls = await asyncio.gather(
        image_service.upload_file(product_data.first_image),
        image_service.upload_file(product_data.second_image),
        image_service.upload_file(product_data.third_image),
    )

    files_to_delete = [product.first_image, product.second_image, product.third_image]
    await asyncio.gather(*[image_service.delete_file(url) for url in files_to_delete])
    product_id = await product_service.update_product(id, product_data, image_urls)
    return SStatusOut(detail=f"product id = {product_id} updated")


@router.post("/add",
             responses ={**UNAUTHORIZED, **NOT_FOUND},
             response_model=SStatusOut,
             summary="Добавить продукт (в Swagger можно добавить только по одной характеристике, добавление нескольких характеристик через /test-form)",
             status_code=status.HTTP_201_CREATED)
async def upload_product(request: Request,
                         response: Response,
                         product_data: SProductIn = Depends(SProductIn.as_form),
                         product_service: ProductsService = Depends(product_service),
                         image_service: S3Service = Depends(s3_service),
                         desk_color_service: SettingsService = Depends(desk_color_service),
                         frame_color_service: SettingsService = Depends(frame_color_service),
                         length_service: SettingsService = Depends(length_service),
                         depth_service: SettingsService = Depends(depth_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    if not await desk_color_service.validate_parameters(product_data.desk_colors):
        raise HTTPException(status_code=400, detail="Invalid desk colors")
    if not await frame_color_service.validate_parameters(product_data.frame_colors):
        raise HTTPException(status_code=400, detail="Invalid frame colors")
    if not await length_service.validate_parameters(product_data.lengths):
        raise HTTPException(status_code=400, detail="Invalid lengths")
    if not await depth_service.validate_parameters(product_data.depths):
        raise HTTPException(status_code=400, detail="Invalid depths")

    image_urls = await asyncio.gather(
        image_service.upload_file(product_data.first_image),
        image_service.upload_file(product_data.second_image),
        image_service.upload_file(product_data.third_image),
    )
    product_id = await product_service.add_product(product_data, image_urls)
    return SStatusOut(detail=f"product id = {product_id} added")