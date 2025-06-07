from fastapi import Depends
from src.repositories.content import ContentRepository
from src.repositories.individual_orders import IndividualOrdersRepository
from src.repositories.products import ProductsRepository
from src.repositories.users import UsersRepository
from src.services.auth import AuthService
from src.services.content import ContentService
from src.services.individual_orders import IndividualOrdersService
from src.services.products import ProductsService
from src.services.s3 import S3Service
from src.services.users import UsersService
from src.repositories.orders import OrdersRepository
from src.repositories.settings import DeskColorsRepository, FrameColorsRepository, LengthRepository, DepthRepository
from src.services.orders import OrdersService
from src.services.settings import SettingsService
from src.utils.config import jwt_config


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

def auth_service(user_service: UsersService = Depends(user_service)):
    return AuthService(private_key_path_read_text=jwt_config.PRIVATE_KEY_PATH.read_text(),
                       public_key_path_read_text=jwt_config.PUBLIC_KEY_PATH.read_text(),
                       algorithm=jwt_config.algorithm,
                       access_token_expire_minutes=jwt_config.access_token_expire_minutes,
                       refresh_token_expire_days=jwt_config.refresh_token_expire_days,
                       user_service=user_service,)