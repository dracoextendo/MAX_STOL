from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.api.dependencies import access_token_validation
from src.api.products import get_all_products

router = APIRouter(prefix="/admin",tags=['HTML', 'Admin'])

@router.get("/login", summary="Страница авторизации (в разработке)")
async def get_login_html():
    pass

@router.get("/", dependencies=[Depends(access_token_validation)], summary="Главная админки (в разработке)")
async def get_admin_html():
    pass

