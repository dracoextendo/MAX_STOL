from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from src.api.dependencies import access_token_validation, order_service, desk_color_service, frame_color_service, \
    length_service, depth_service, content_service, individual_order_service
from src.api.responses import HTML_RESPONSE
from src.services.content import ContentService
from src.services.individual_orders import IndividualOrdersService
from src.services.orders import OrdersService
from src.services.products import ProductsService
from src.api.dependencies import product_service
from src.services.settings import SettingsService

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory='./templates/admin')

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
async def get_admin_html(request: Request, orders_service: OrdersService = Depends(order_service)):
    orders = await orders_service.get_all_orders()
    return templates.TemplateResponse("orders.html", context={'request': request, 'orders': orders})

@router.get("/desks",
            dependencies=[Depends(access_token_validation)],
            summary="Продукты",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, product_service: ProductsService = Depends(product_service)):
    products = await product_service.get_all_products(order_by=["sort", "id"])
    return templates.TemplateResponse("products.html", context={'request': request, 'products': products})

@router.get("/desk-colors",
            dependencies=[Depends(access_token_validation)],
            summary="Цвета столешниц",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, desk_color_service: SettingsService = Depends(desk_color_service)):
    desk_colors = await desk_color_service.get_all_parameters()
    return templates.TemplateResponse("desk-colors.html", context={'request': request, 'desk_colors': desk_colors})

@router.get("/frame-colors",
            dependencies=[Depends(access_token_validation)],
            summary="Цвета металлокаркаса",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, frame_color_service: SettingsService = Depends(frame_color_service)):
    frame_colors = await frame_color_service.get_all_parameters()
    return templates.TemplateResponse("frame-colors.html", context={'request': request, 'frame_colors': frame_colors})

@router.get("/lengths",
            dependencies=[Depends(access_token_validation)],
            summary="Длины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, length_service: SettingsService = Depends(length_service)):
    lengths = await length_service.get_all_parameters()
    return templates.TemplateResponse("lengths.html", context={'request': request, 'lengths': lengths})

@router.get("/depths",
            dependencies=[Depends(access_token_validation)],
            summary="Глубины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, depth_service: SettingsService = Depends(depth_service)):
    depths = await depth_service.get_all_parameters()
    return templates.TemplateResponse("depths.html", context={'request': request, 'depths': depths})

@router.get("/content",
            dependencies=[Depends(access_token_validation)],
            summary="Настройки контента",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, content_service: ContentService = Depends(content_service)):
    content = await content_service.get_content()
    return templates.TemplateResponse("content.html", context={'request': request, 'content': content})

@router.get("/individual-project",
            dependencies=[Depends(access_token_validation)],
            summary="Заявки на индивидуальный проект",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_admin_html(request: Request, individual_order_service: IndividualOrdersService = Depends(individual_order_service)):
    orders = await individual_order_service.get_all_orders()
    return templates.TemplateResponse("individual-project.html", context={'request': request, 'orders': orders})

