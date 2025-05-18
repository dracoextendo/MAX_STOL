import datetime
import bcrypt
import jwt
from src.config import jwt_config

def encode_jwt(payload: dict,
               private_key: str = jwt_config.PRIVATE_KEY_PATH.read_text(),
               algorithm: str= jwt_config.algorithm,
               expire_minutes: int = jwt_config.access_token_expire_minutes,):
    now = datetime.datetime.now(datetime.UTC)
    expire = now + datetime.timedelta(minutes=expire_minutes)
    payload.update(exp=expire,
                   iat=now,)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded

def decode_jwt(token: str | bytes, public_key: str = jwt_config.PUBLIC_KEY_PATH.read_text(), algorithm: str= jwt_config.algorithm):
    decoded = jwt.decode(token, public_key, algorithms=algorithm)
    return decoded

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)

def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())