from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from src.api.dependencies import user_service, auth_service
from src.utils.responses import UNAUTHORIZED
from src.schemas.base import SStatusOut
from src.schemas.users import SUserIn
from src.services.auth import AuthService
from src.services.users import UsersService
from src.utils.config import SECURE_COOKIE

router = APIRouter(tags=['Auth'])

@router.post('/auth',
             summary="Авторизация",
             responses ={**UNAUTHORIZED},
             response_model=SStatusOut)
async def auth(response: Response,
               user_data: SUserIn = Depends(SUserIn.as_form),
               user_service: UsersService = Depends(user_service),
               auth_service: AuthService = Depends(auth_service)):
    user = await user_service.get_user_by_username(user_data.username)
    if not user or not auth_service.validate_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth_service.create_access_token(user)
    refresh_token = auth_service.create_refresh_token(user)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'  # Защита от CSRF
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=SECURE_COOKIE,
        samesite='lax'  # Защита от CSRF
    )
    return SStatusOut(detail="Authenticated successfully")

@router.post('/logout', summary="Выход", response_model=SStatusOut)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}