from typing import Annotated

import bcrypt
from fastapi import APIRouter, Form, HTTPException, Response
from src.dao.dao import UsersDAO
from src.security import security
router = APIRouter(tags=['Auth'])


@router.post('/login')
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    user = await UsersDAO.get_user(username)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = security.create_access_token(uid=str(user.id))
    security.set_access_cookies(token=access_token, response=response)
    return {"access_token": access_token}
