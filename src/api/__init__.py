from fastapi import APIRouter
from src.api.products import router as products_router
from src.api.orders import router as orders_router
from src.api.root import router as root_router
from src.api.auth import router as auth_router
from src.api.admin import router as admin_router
from src.api.desk_settings import router as settings_router
from src.api.individual_orders import router as individual_orders_router

main_router = APIRouter()
main_router.include_router(root_router)
main_router.include_router(auth_router)
main_router.include_router(admin_router)
main_router.include_router(products_router)
main_router.include_router(orders_router)
main_router.include_router(individual_orders_router)
main_router.include_router(settings_router)