import datetime
import jwt
import bcrypt
from jwt import ExpiredSignatureError


class AuthService:
    def __init__(self, private_key_path_read_text, public_key_path_read_text, algorithm, access_token_expire_minutes, refresh_token_expire_days, user_service):
        self.private_key = private_key_path_read_text
        self.public_key = public_key_path_read_text
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.user_service = user_service

    def encode_jwt(self, payload: dict, expire_timedelta: datetime.timedelta | None = None) -> str:
        now = datetime.datetime.now(datetime.UTC)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + datetime.timedelta(minutes=self.access_token_expire_minutes)
        payload.update(exp=expire,
                       iat=now, )
        encoded = jwt.encode(payload, self.private_key, algorithm=self.algorithm)
        return encoded

    def decode_jwt(self, token: str | bytes):
        decoded = jwt.decode(token, self.public_key, algorithms=self.algorithm)
        return decoded

    @staticmethod
    def hash_password(password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt)

    @staticmethod
    def validate_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    def create_jwt(self,
                   token_type: str,
                   payload: dict,
                   expire_timedelta: datetime.timedelta | None = None) -> str:
        jwt_payload = {"type": token_type}
        jwt_payload.update(payload)
        return self.encode_jwt(payload=jwt_payload, expire_timedelta=expire_timedelta)

    def create_access_token(self, user):
        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
        }
        return self.create_jwt(token_type="access",
                          payload=jwt_payload,
                          )

    def create_refresh_token(self, user):
        jwt_payload = {
            "sub": str(user.id),
        }
        return self.create_jwt(token_type="refresh",
                          payload=jwt_payload,
                          expire_timedelta=datetime.timedelta(days=self.refresh_token_expire_days),
                          )

    async def validate_access_token(self, access_token: str, refresh_token: str | None = None) -> bool | str:
        if not access_token:
            return False
        else:
            try:
                payload = self.decode_jwt(access_token)
                token_type = payload.get("type")
                if token_type != "access":
                    return False
                return access_token
            except ExpiredSignatureError:
                new_token = await self.refresh_access_token(refresh_token)
                if new_token:
                    return new_token
                return False
            except Exception:
                return False

    async def refresh_access_token(self, refresh_token) -> None | str:
        if not refresh_token:
            return None
        try:
            payload = self.decode_jwt(refresh_token)
            token_type = payload.get("type")
            if token_type != "refresh":
                return None
            user_id = int(payload.get("sub"))
            user = await self.user_service.get_user(user_id)
            new_access_token = self.create_access_token(user)
            return new_access_token
        except Exception:
            return None
