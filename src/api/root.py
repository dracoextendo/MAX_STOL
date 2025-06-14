from pathlib import Path
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.api.dependencies import content_service
from src.api.products import get_all_active_products
from src.utils.responses import HTML_RESPONSE
from src.services.content import ContentService

router = APIRouter(tags=['HTML'], responses={**HTML_RESPONSE})

templates_path = Path(__file__).parent.parent / "templates"

templates = Jinja2Templates(directory=templates_path)

@router.get("/", summary="Главная страница", response_class=HTMLResponse)
async def get_index_html(request: Request,
                         products=Depends(get_all_active_products),
                         content_service: ContentService = Depends(content_service)):
    content = await content_service.get_content()
    return templates.TemplateResponse(request=request, name="index.html", context={'products': products, 'content': content})

@router.get("/test-form", summary="Тестовая форма для создания продукта", response_class=HTMLResponse)
async def get_test_form_html(request: Request):
    return templates.TemplateResponse("test-form.html", context={'request': request})