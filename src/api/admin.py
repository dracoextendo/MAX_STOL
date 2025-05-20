from fastapi import APIRouter, Depends
from src.api.dependencies import access_token_validation

router = APIRouter(prefix="/admin",tags=['HTML', 'Admin'])

@router.get("/login", summary="Страница авторизации (в разработке)")
async def get_login_html():
    pass

@router.get("/", dependencies=[Depends(access_token_validation)], summary="Главная админки (в разработке)")
async def get_admin_html():
    pass

