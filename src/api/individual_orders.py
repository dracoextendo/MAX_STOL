from fastapi import APIRouter, HTTPException, Depends, status
from src.api.dependencies import access_token_validation, individual_order_service
from src.api.responses import UNAUTHORIZED, FORBIDDEN, NOT_FOUND
from src.schemas.base import SStatusOut
from src.schemas.individual_orders import SIndividualOrderOut, SIndividualOrderIn
from src.services.individual_orders import IndividualOrdersService

router = APIRouter(tags=['Индивидуальные заказы'], prefix='/individual-orders')

@router.get("",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN},
            response_model=list[SIndividualOrderOut],
            summary="Получить все заказы")
async def get_all_orders(order_service: IndividualOrdersService = Depends(individual_order_service)):
    orders = await order_service.get_all_orders()
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders

@router.get("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SIndividualOrderOut,
            summary="Получить информацию о заказе по id")
async def get_order_by_id(id: int, order_service: IndividualOrdersService = Depends(individual_order_service)):
    order = await order_service.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{id}",
               dependencies=[Depends(access_token_validation)],
               responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить заказ")
async def delete_order(id: int, order_service: IndividualOrdersService = Depends(individual_order_service)):
    order_id = await order_service.delete_order(id)
    if not order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return SStatusOut(detail=f"Order id = {order_id} deleted")

@router.put("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить заказ")
async def update_order(id:int, order: SIndividualOrderIn = Depends(SIndividualOrderIn.as_form), order_service: IndividualOrdersService = Depends(individual_order_service)):
    order_id = await order_service.update_order(id, order)
    if not order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return SStatusOut(detail=f"Order id = {order_id} updated")

@router.post("/add",
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить заказ",) # нужно продумать защиту через куки
async def add_order(order: SIndividualOrderIn = Depends(SIndividualOrderIn.as_form), order_service: IndividualOrdersService = Depends(individual_order_service)):
    order_id = await order_service.add_order(order)
    return SStatusOut(detail=f"Order id = {order_id} added")