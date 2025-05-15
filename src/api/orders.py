from fastapi import APIRouter, HTTPException, Depends
from src.dao.dao import OrdersDAO
from src.schemas.base import SBaseStatus
from src.schemas.orders import SCreateOrder, SGetOrder
from src.security import security

router = APIRouter(tags=['Заказы'], prefix='/orders')

@router.get("", dependencies=[Depends(security.access_token_required)], response_model=list[SGetOrder], summary="Получить все заказы")
async def get_all_orders():
    return await OrdersDAO().find_all()

@router.get("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SGetOrder, summary="Получить информацию о заказе по id")
async def get_all_orders(id: int):
    result = await OrdersDAO.get_order(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.delete("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Удалить заказ (в разработке)")
async def update_product():
    return {"status": "success"}

@router.put("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Обновить заказ (в разработке)")
async def update_product():
    return {"status": "success"}

@router.post("/add", response_model=SBaseStatus, summary="Добавить заказ (в разработке)")
async def add_order(order: SCreateOrder):
    return {"status": "success"}
