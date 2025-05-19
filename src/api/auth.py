from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Response
from fastapi.params import Depends
from src.api.dependencies import get_user_for_refresh
from src.dao.dao import UsersDAO
import src.security as security

router = APIRouter(tags=['Auth'])


@router.post('/auth', summary="Авторизация")
async def auth(username: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    user = await UsersDAO.get_user(username)
    if user and security.validate_password(password, user.hashed_password):
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
        return {"message": "Authenticated successfully"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.post('/refresh', summary="Refresh token")
def refresh_token(response: Response, user = Depends(get_user_for_refresh)):
    if user:
        access_token = security.create_access_token(user)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,  # Только HTTPS
            samesite='lax'  # Защита от CSRF
        )
        return {"message": "Token refresh successfully"}
    return {"message": "Cant refresh token"}


@router.post('/logout', summary="Выход")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}