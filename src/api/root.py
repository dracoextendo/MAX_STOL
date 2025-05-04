from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.api.products import get_products

router = APIRouter()
templates = Jinja2Templates(directory='./templates')

@router.get("/")
async def get_index_html(request: Request, products=Depends(get_products)):
    return templates.TemplateResponse("index.html", context={'request': request, 'products': products})