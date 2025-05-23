from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Response
from fastapi.params import Depends
from src.api.responses import UNAUTHORIZED, FORBIDDEN
from src.dao.dao import UsersDAO
import src.security as security
from src.schemas.base import SStatusOut
from src.schemas.users import SUserIn

router = APIRouter(tags=['Auth'])

@router.post('/auth',
             summary="Авторизация",
             responses ={**UNAUTHORIZED},
             response_model=SStatusOut)
async def auth(response: Response, user_data: SUserIn = Depends(SUserIn.as_form)):
    user = await UsersDAO.get_user_by_username(user_data.username)
    if user and security.validate_password(user_data.password, user.hashed_password):
        access_token = security.create_access_token(user)
        refresh_token = security.create_refresh_token(user)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Только HTTPS
            samesite='lax'  # Защита от CSRF
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,  # Только HTTPS
            samesite='lax'  # Защита от CSRF
        )
        return SStatusOut(detail="Authenticated successfully")
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.post('/logout', summary="Выход", response_model=SStatusOut)
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"detail": "Logged out"}