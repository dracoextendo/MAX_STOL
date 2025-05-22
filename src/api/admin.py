from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from src.api.dependencies import access_token_validation
from src.api.responses import HTML_RESPONSE

router = APIRouter(prefix="/admin",tags=['HTML', 'Admin'], responses={**HTML_RESPONSE})

@router.get("/login", summary="Страница авторизации (в разработке)", response_class=HTMLResponse)
async def get_login_html():
    pass

@router.get("/", dependencies=[Depends(access_token_validation)], summary="Главная админки (в разработке)", response_class=HTMLResponse)
async def get_admin_html():
    pass

