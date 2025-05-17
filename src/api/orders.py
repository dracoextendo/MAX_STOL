from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Form
from watchfiles import awatch

from src.dao.dao import OrdersDAO
from src.models.orders import OrdersModel
from src.schemas.base import SBaseStatus
from src.schemas.orders import SCreateOrder, SGetOrder
from src.security import security

router = APIRouter(tags=['Заказы'], prefix='/orders')

@router.get("", dependencies=[Depends(security.access_token_required)], response_model=list[SGetOrder], summary="Получить все заказы")
async def get_all_orders():
    return await OrdersDAO().find_all()

@router.get("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SGetOrder, summary="Получить информацию о заказе по id")
async def get_order_by_id(id: int):
    result = await OrdersDAO.get_order(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.delete("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Удалить заказ")
async def delete_order(id: int):
    return await OrdersDAO.delete_order(id)

@router.put("/{id}", dependencies=[Depends(security.access_token_required)], response_model=SBaseStatus, summary="Обновить заказ")
async def update_order(id:int,
                    username: Annotated[str, Form()],
                    phone: Annotated[str, Form()],
                    email: Annotated[str | None, Form()],
                    telegram: Annotated[str | None, Form()],
                    product_name: Annotated[str, Form()],
                    desk_color: Annotated[str, Form()],
                    frame_color: Annotated[str, Form()],
                    depth: Annotated[str, Form()],
                    length: Annotated[str, Form()]):
    order = OrdersModel(
        username=username,
        phone=phone,
        email=email,
        telegram=telegram,
        product_name=product_name,
        desk_color=desk_color,
        frame_color=frame_color,
        depth=depth,
        length=length,
    )
    return await OrdersDAO().update_order(id, order)

@router.post("/add", response_model=SBaseStatus, summary="Добавить заказ") # нужно продумать защиту через куки
async def add_order(username: Annotated[str, Form()],
                    phone: Annotated[str, Form()],
                    email: Annotated[str | None, Form()],
                    telegram: Annotated[str | None, Form()],
                    product_name: Annotated[str, Form()],
                    desk_color: Annotated[str, Form()],
                    frame_color: Annotated[str, Form()],
                    depth: Annotated[str, Form()],
                    length: Annotated[str, Form()]):
    order = OrdersModel(
        username=username,
        phone=phone,
        email=email,
        telegram=telegram,
        product_name=product_name,
        desk_color=desk_color,
        frame_color=frame_color,
        depth=depth,
        length=length,
    )
    return await OrdersDAO.add_order(order)