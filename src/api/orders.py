from fastapi import APIRouter, HTTPException

from src.dao.dao import OrdersDAO
from src.schemas.base import SBaseStatus
from src.schemas.orders import SCreateOrder, SGetOrder

router = APIRouter(tags=['Заказ'], prefix='/order')

@router.get("/get_all", response_model=list[SGetOrder], summary="Получить все заказы")
async def get_all_orders():
    return await OrdersDAO().find_all()

@router.get("/{id}", response_model=SGetOrder, summary="Получить информацию о заказе по id")
async def get_all_orders(id: int):
    result = await OrdersDAO.get_order(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.post("/add", response_model=SBaseStatus, summary="Добавить заказ (в разработке)")
async def add_order(order: SCreateOrder):
    return {"status": "success"}
