import datetime
import bcrypt
import jwt
from src.config import jwt_config

def encode_jwt(payload: dict,
               private_key: str = jwt_config.PRIVATE_KEY_PATH.read_text(),
               algorithm: str= jwt_config.algorithm,
               expire_minutes: int = jwt_config.access_token_expire_minutes,
               expire_timedelta: datetime.timedelta | None = None) -> str:
    now = datetime.datetime.now(datetime.UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
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

def create_jwt(token_type: str,
               payload: dict,
               expire_minutes: int = jwt_config.access_token_expire_minutes,
               expire_timedelta: datetime.timedelta | None = None) -> str:
    jwt_payload = {"type": token_type}
    jwt_payload.update(payload)
    return encode_jwt(payload=jwt_payload,
                      expire_minutes=expire_minutes,
                      expire_timedelta=expire_timedelta
                      )

def create_access_token(user):
    jwt_payload = {
        "sub": str(user.id),
        "username": user.username,
    }
    return create_jwt(token_type="access",
                      payload=jwt_payload,
                      expire_minutes=jwt_config.access_token_expire_minutes,
                      )

def create_refresh_token(user):
    jwt_payload = {
        "sub": str(user.id),
    }
    return create_jwt(token_type="refresh",
                      payload=jwt_payload,
                      expire_timedelta=datetime.timedelta(days=jwt_config.refresh_token_expire_days),
                      )
