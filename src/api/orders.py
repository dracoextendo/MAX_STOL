from fastapi import APIRouter

from src.schemas.orders import SCreateOrder

router = APIRouter(tags=['Заказ'])

@router.post("/create_order")
async def create_order(order: SCreateOrder):
    return order

