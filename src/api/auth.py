import uuid
from typing import Annotated

import bcrypt
from fastapi import APIRouter, Form, HTTPException, Response
from src.dao.dao import UsersDAO
import src.security as security

router = APIRouter(tags=['Auth'])


@router.post('/auth', summary="Авторизация")
async def auth(username: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    user = await UsersDAO.get_user(username)
    if user and security.validate_password(password, user.hashed_password):
        jwt_payload = {
            "sub": str(user.id),
            "username": user.username,
            "email": user.email,
        }
        token = security.encode_jwt(jwt_payload)
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=False,  # Только HTTPS
            samesite='lax'  # Защита от CSRF
        )
        return {"message": "Authenticated successfully"}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@router.post('/logout', summary="Выход (в разработке)")
async def logout():
    pass