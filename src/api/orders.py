from fastapi import APIRouter, HTTPException, Depends, status
from src.api.dependencies import access_token_validation, order_service
from src.api.responses import UNAUTHORIZED, FORBIDDEN, NOT_FOUND
from src.schemas.base import SStatusOut
from src.schemas.orders import SOrderOut, SOrderIn
from src.services.orders import OrdersService


router = APIRouter(tags=['Заказы'], prefix='/orders')

@router.get("",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN},
            response_model=list[SOrderOut],
            summary="Получить все заказы")
async def get_all_orders(order_service: OrdersService = Depends(order_service)):
    orders = await order_service.get_all_orders()
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders

@router.get("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SOrderOut,
            summary="Получить информацию о заказе по id")
async def get_order_by_id(id: int, order_service: OrdersService = Depends(order_service)):
    order = await order_service.orders_repository.get_one(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{id}",
               dependencies=[Depends(access_token_validation)],
               responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить заказ")
async def delete_order(id: int, order_service: OrdersService = Depends(order_service)):
    order_id = await order_service.delete_order(id)
    if not order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return SStatusOut(detail=f"Order id = {order_id} deleted")

@router.put("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить заказ")
async def update_order(id:int, order: SOrderIn = Depends(SOrderIn.as_form), order_service: OrdersService = Depends(order_service)):
    order_id = await order_service.update_order(id, order)
    if not order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return SStatusOut(detail=f"Order id = {order_id} updated")

@router.post("/add",
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить заказ",) # нужно продумать защиту через куки
async def add_order(order: SOrderIn = Depends(SOrderIn.as_form), order_service: OrdersService = Depends(order_service)):
    order_id = await order_service.add_order(order)
    return SStatusOut(detail=f"Order id = {order_id} added")
