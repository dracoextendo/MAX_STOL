from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from src.api.dependencies import individual_order_service, auth_service
from src.utils.responses import UNAUTHORIZED, NOT_FOUND
from src.schemas.base import SStatusOut
from src.schemas.individual_orders import SIndividualOrderOut, SIndividualOrderIn
from src.services.auth import AuthService
from src.services.individual_orders import IndividualOrdersService
from src.utils.config import SECURE_COOKIE

router = APIRouter(tags=['Индивидуальные заказы'], prefix='/individual-orders')

@router.get("",
            responses={**UNAUTHORIZED},
            response_model=list[SIndividualOrderOut],
            summary="Получить все заказы")
async def get_all_orders(request: Request,
                         response: Response,
                         order_service: IndividualOrdersService = Depends(individual_order_service),
                         auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,)
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    orders = await order_service.get_all_orders()
    if not orders:
        raise HTTPException(status_code=404, detail="Orders not found")
    return orders

@router.get("/{id}",
            responses ={**UNAUTHORIZED, **NOT_FOUND},
            response_model=SIndividualOrderOut,
            summary="Получить информацию о заказе по id")
async def get_order_by_id(request: Request,
                          response: Response,
                          id: int,
                          order_service: IndividualOrdersService = Depends(individual_order_service),
                          auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    order = await order_service.get_order(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.delete("/{id}",
               responses={**UNAUTHORIZED, **NOT_FOUND},
               response_model=SStatusOut,
               summary="Удалить заказ")
async def delete_order(request: Request,
                       response: Response,
                       id: int, order_service: IndividualOrdersService = Depends(individual_order_service),
                       auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
    order_id = await order_service.delete_order(id)
    if not order_id:
        raise HTTPException(status_code=404, detail="Order not found")
    return SStatusOut(detail=f"Order id = {order_id} deleted")

@router.put("/{id}",
            responses={**UNAUTHORIZED, **NOT_FOUND},
            response_model=SStatusOut,
            summary="Обновить заказ")
async def update_order(request: Request,
                       response: Response,
                       id:int,
                       order: SIndividualOrderIn = Depends(SIndividualOrderIn.as_form),
                       order_service: IndividualOrdersService = Depends(individual_order_service),
                       auth_service: AuthService = Depends(auth_service)):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    refreshed_token = await auth_service.validate_access_token(access_token, refresh_token)
    if not refreshed_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )
    response.set_cookie(
        key="access_token",
        value=refreshed_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'
    )
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