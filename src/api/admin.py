from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates
from src.api.dependencies import order_service, desk_color_service, frame_color_service, \
    length_service, depth_service, content_service, individual_order_service, auth_service
from src.utils.responses import HTML_RESPONSE
from src.services.auth import AuthService
from src.services.content import ContentService
from src.services.individual_orders import IndividualOrdersService
from src.services.orders import OrdersService
from src.services.products import ProductsService
from src.api.dependencies import product_service
from src.services.settings import SettingsService
from src.utils.config import SECURE_COOKIE

router = APIRouter(prefix="/admin")
templates = Jinja2Templates(directory='./templates/admin')

@router.get("/login",
            summary="Страница авторизации",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_login_html(request: Request,
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return templates.TemplateResponse("login.html", context={'request': request})
    return RedirectResponse(url="/admin")

@router.get("",
            summary="Главная админки (заказы)",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_orders_html(request: Request,
                          order_service: OrdersService = Depends(order_service),
                          auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    orders = await order_service.get_all_orders(order_by="-created_at")
    response = templates.TemplateResponse("orders.html", context={'request': request, 'orders': orders})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/desks",
            summary="Продукты",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_products_html(request: Request,
                            product_service: ProductsService = Depends(product_service),
                            auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    products = await product_service.get_all_products(order_by=["sort", "id"])
    response = templates.TemplateResponse("products.html", context={'request': request, 'products': products})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/desk-colors",
            summary="Цвета столешниц",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_desk_colors_html(request: Request,
                         desk_color_service: SettingsService = Depends(desk_color_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    desk_colors = await desk_color_service.get_all_parameters()
    response = templates.TemplateResponse("desk-colors.html", context={'request': request, 'desk_colors': desk_colors})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/frame-colors",
            summary="Цвета металлокаркаса",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_frame_colors_html(request: Request,
                         frame_color_service: SettingsService = Depends(frame_color_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    frame_colors = await frame_color_service.get_all_parameters()
    response = templates.TemplateResponse("frame-colors.html", context={'request': request, 'frame_colors': frame_colors})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/lengths",
            summary="Длины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_lengths_html(request: Request,
                         length_service: SettingsService = Depends(length_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    lengths = await length_service.get_all_parameters()
    response = templates.TemplateResponse("lengths.html", context={'request': request, 'lengths': lengths})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/depths",
            summary="Глубины столов",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_depths_html(request: Request,
                         depth_service: SettingsService = Depends(depth_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    depths = await depth_service.get_all_parameters()
    response = templates.TemplateResponse("depths.html", context={'request': request, 'depths': depths})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/content",
            summary="Настройки контента",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_content_html(request: Request,
                         content_service: ContentService = Depends(content_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    content = await content_service.get_content()
    response = templates.TemplateResponse("content.html", context={'request': request, 'content': content})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

@router.get("/individual-project",
            summary="Заявки на индивидуальный проект",
            response_class=HTMLResponse,
            responses={**HTML_RESPONSE},
            tags=['HTML', 'Admin'])
async def get_individual_order_html(request: Request,
                         individual_order_service: IndividualOrdersService = Depends(individual_order_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        return RedirectResponse(url="/admin/login")
    individual_orders = await individual_order_service.get_all_orders(order_by="-created_at")
    response = templates.TemplateResponse("individual-project.html", context={'request': request, 'orders': individual_orders})
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    return response

