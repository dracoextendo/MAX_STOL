from fastapi import APIRouter

from src.schemas.orders import SCreateOrder

router = APIRouter()

@router.post("/create_order")
async def create_order(order: SCreateOrder):
    return order

