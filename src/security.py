from datetime import timedelta

from authx import AuthX, AuthXConfig

from src.config import JWTConfig

jwt_config = JWTConfig()

config = AuthXConfig()
config.JWT_SECRET_KEY = jwt_config.jwt_secret.get_secret_value()
config.JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=1)
config.JWT_ACCESS_COOKIE_NAME="access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False # изменить на True на продакшене

security = AuthX(config=config)
