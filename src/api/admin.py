from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse

from src.api.dependencies import access_token_validation
from src.api.responses import HTML_RESPONSE, NOT_FOUND
from src.dao.dao import ProductsDAO
from src.schemas.products import SProductOut, SProductInfoOut

router = APIRouter(prefix="/admin")

@router.get("/login",
            summary="Страница авторизации (в разработке)",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_login_html():
    pass

@router.get("/products",
            dependencies=[Depends(access_token_validation)],
            response_model=list[SProductOut],
            summary="Получить все продукты (активные и неактивные)",
            tags=['Admin'])
async def get_all_products():
    return await ProductsDAO().find_all()

@router.get("/products/{id}",
            responses ={**NOT_FOUND},
            dependencies=[Depends(access_token_validation)],
            response_model=SProductInfoOut,
            summary="Получить информацию о продукте по id",
            tags=['Admin'])
async def get_product_by_id(id: int):
    result = await ProductsDAO.get_product(id, False)
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return result

@router.get("",
            dependencies=[Depends(access_token_validation)],
            summary="Главная админки (в разработке)",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html():
    pass

