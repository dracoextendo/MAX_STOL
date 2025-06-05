from fastapi import Request, HTTPException, Response
from jwt import ExpiredSignatureError

from src.repositories.content import ContentRepository
from src.repositories.individual_orders import IndividualOrdersRepository
from src.repositories.products import ProductsRepository
from src.repositories.users import UsersRepository
from src.services.content import ContentService
from src.services.individual_orders import IndividualOrdersService
from src.services.products import ProductsService
from src.services.s3 import S3Service
from src.services.users import UsersService
from src.utils import security
from src.repositories.orders import OrdersRepository
from src.repositories.settings import DeskColorsRepository, FrameColorsRepository, LengthRepository, DepthRepository
from src.services.orders import OrdersService
from src.services.settings import SettingsService


def product_service():
    return ProductsService(ProductsRepository)

def order_service():
    return OrdersService(OrdersRepository)

def individual_order_service():
    return IndividualOrdersService(IndividualOrdersRepository)

def desk_color_service():
    return SettingsService(DeskColorsRepository)

def frame_color_service():
    return SettingsService(FrameColorsRepository)

def length_service():
    return SettingsService(LengthRepository)

def depth_service():
    return SettingsService(DepthRepository)

def user_service():
    return UsersService(UsersRepository)

def content_service():
    return ContentService(ContentRepository)

def s3_service():
    return S3Service()

async def access_token_validation(request: Request, response: Response):
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    if not access_token:
        raise HTTPException(
            status_code=307,
            detail="Unauthorized",
            headers={"Location": "/admin/login"}
        )
    if access_token:
        try:
            payload = security.decode_jwt(access_token)
            token_type = payload.get("type")
            if token_type != "access":
                raise HTTPException(
                    status_code=307,
                    detail="Unauthorized",
                    headers={"Location": "/admin/login"}
                )
            return None
        except ExpiredSignatureError:
            pass
        except Exception:
            raise HTTPException(
                status_code=307,
                detail="Unauthorized",
                headers={"Location": "/admin/login"}
            )
    try:
        payload = security.decode_jwt(refresh_token)
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=307,
                detail="Unauthorized",
                headers={"Location": "/admin/login"}
            )
        user_id = int(payload.get("sub"))
        user = await user_service().get_user(user_id)
        new_access_token = security.create_access_token(user)
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax"
        )
        return None
    except Exception:
        raise HTTPException(
            status_code=307,
            detail="Unauthorized",
            headers={"Location": "/admin/login"}
        )