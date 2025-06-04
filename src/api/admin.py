from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.api.dependencies import access_token_validation
from src.api.orders import get_all_orders
from src.api.responses import HTML_RESPONSE, NOT_FOUND
from src.api.settings import get_all_desk_colors, get_all_frame_colors, get_all_lengths, get_all_depths
from src.dao.dao import ProductsDAO, ContentDAO, IndividualOrdersDAO
from src.schemas.products import SProductOut, SProductInfoOut

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory='./admin/templates')

@router.get("/products",
            dependencies=[Depends(access_token_validation)],
            response_model=list[SProductOut],
            summary="Получить все продукты (активные и неактивные)",
            tags=['Admin'])
async def get_all_products_admin():
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

@router.get("/login",
            summary="Страница авторизации",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_login_html(request: Request):
    return templates.TemplateResponse("login.html", context={'request': request})

@router.get("",
            dependencies=[Depends(access_token_validation)],
            summary="Главная админки (заказы)",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, orders=Depends(get_all_orders)):
    return templates.TemplateResponse("orders.html", context={'request': request, 'orders': orders})

@router.get("/desks",
            dependencies=[Depends(access_token_validation)],
            summary="Продукты",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, products=Depends(get_all_products_admin)):
    return templates.TemplateResponse("products.html", context={'request': request, 'products': products})

@router.get("/desk-colors",
            dependencies=[Depends(access_token_validation)],
            summary="Цвета столешниц",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, desk_colors=Depends(get_all_desk_colors)):
    return templates.TemplateResponse("desk-colors.html", context={'request': request, 'desk_colors': desk_colors})

@router.get("/frame-colors",
            dependencies=[Depends(access_token_validation)],
            summary="Цвета металлокаркаса",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, frame_colors=Depends(get_all_frame_colors)):
    return templates.TemplateResponse("frame-colors.html", context={'request': request, 'frame_colors': frame_colors})

@router.get("/lengths",
            dependencies=[Depends(access_token_validation)],
            summary="Длины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, lengths=Depends(get_all_lengths)):
    return templates.TemplateResponse("lengths.html", context={'request': request, 'lengths': lengths})

@router.get("/depths",
            dependencies=[Depends(access_token_validation)],
            summary="Глубины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, depths=Depends(get_all_depths)):
    return templates.TemplateResponse("depths.html", context={'request': request, 'depths': depths})

@router.get("/content",
            dependencies=[Depends(access_token_validation)],
            summary="Настройки контента",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, content=Depends(ContentDAO.find_first)):
    return templates.TemplateResponse("content.html", context={'request': request, 'content': content})

@router.get("/individual-project",
            dependencies=[Depends(access_token_validation)],
            summary="Заявки на индивидуальный проект",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, orders=Depends(IndividualOrdersDAO.find_all)):
    return templates.TemplateResponse("individual-project.html", context={'request': request, 'orders': orders})

