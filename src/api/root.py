from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from src.api.products import get_all_products
from src.api.responses import HTML_RESPONSE

router = APIRouter(tags=['HTML'], responses={**HTML_RESPONSE})

templates = Jinja2Templates(directory='./templates')

@router.get("/", summary="Главная страница", response_class=HTMLResponse)
async def get_index_html(request: Request, products=Depends(get_all_products)):
    return templates.TemplateResponse("index.html", context={'request': request, 'products': products})

@router.get("/test-form", summary="Тестовая форма для создания продукта", response_class=HTMLResponse)
async def get_index_html(request: Request):
    return templates.TemplateResponse("test-form.html", context={'request': request})