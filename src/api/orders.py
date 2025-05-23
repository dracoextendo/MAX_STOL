from fastapi import APIRouter, HTTPException, Depends, status, Response
from src.api.dependencies import access_token_validation
from src.api.responses import UNAUTHORIZED, FORBIDDEN, NOT_FOUND
from src.dao.dao import OrdersDAO
from src.models.orders import OrdersModel
from src.schemas.base import SStatusOut
from src.schemas.orders import SOrderOut, SOrderIn

router = APIRouter(tags=['Заказы'], prefix='/orders')

@router.get("",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN},
            response_model=list[SOrderOut],
            summary="Получить все заказы")
async def get_all_orders():
    return await OrdersDAO().find_all()

@router.get("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses ={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SOrderOut,
            summary="Получить информацию о заказе по id")
async def get_order_by_id(id: int):
    result = await OrdersDAO.get_order(id)
    if result is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return result

@router.delete("/{id}",
               dependencies=[Depends(access_token_validation)],
               responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить заказ")
async def delete_order(id: int):
    return await OrdersDAO.delete_order(id)

@router.put("/{id}",
            dependencies=[Depends(access_token_validation)],
            responses={**UNAUTHORIZED, **FORBIDDEN, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить заказ")
async def update_order(id:int, order_data: SOrderIn = Depends(SOrderIn.as_form)):
    order = OrdersModel(
        username=order_data.username,
        phone=order_data.phone,
        email=order_data.email,
        telegram=order_data.telegram,
        product_name=order_data.product_name,
        desk_color=order_data.desk_color,
        frame_color=order_data.frame_color,
        depth=order_data.depth,
        length=order_data.length,
    )
    return await OrdersDAO().update_order(id, order)

@router.post("/add",
             responses={**UNAUTHORIZED, **FORBIDDEN},
             response_model=SStatusOut,
             status_code=status.HTTP_201_CREATED,
             summary="Добавить заказ",) # нужно продумать защиту через куки
async def add_order(order_data: SOrderIn = Depends(SOrderIn.as_form)):
    order = OrdersModel(
        username=order_data.username,
        phone=order_data.phone,
        email=order_data.email,
        telegram=order_data.telegram,
        product_name=order_data.product_name,
        desk_color=order_data.desk_color,
        frame_color=order_data.frame_color,
        depth=order_data.depth,
        length=order_data.length,
    )
    return await OrdersDAO.add_order(order)