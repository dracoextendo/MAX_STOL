from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from src.api.products import get_all_products

router = APIRouter(tags=['HTML'])

templates = Jinja2Templates(directory='./templates')

@router.get("/", summary="Главная страница")
async def get_index_html(request: Request, products=Depends(get_all_products)):
    return templates.TemplateResponse("index.html", context={'request': request, 'products': products})

@router.get("/test-form", summary="Тестовая форма для создания продукта")
async def get_index_html(request: Request):
    return templates.TemplateResponse("test-form.html", context={'request': request})