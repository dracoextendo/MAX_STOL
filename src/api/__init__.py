from fastapi import APIRouter

from src.api.products import router as products_router
from src.api.orders import router as orders_router
from src.api.root import router as root_router

main_router = APIRouter()
main_router.include_router(products_router)
main_router.include_router(orders_router)
main_router.include_router(root_router)