from fastapi import Request, HTTPException
from src import security
from src.dao.dao import UsersDAO


def access_token_validation(request: Request):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = security.decode_jwt(access_token)
        token_type = payload.get("type")
        if token_type != "access":
            raise HTTPException(status_code=401, detail="Not authenticated")
    except Exception:
        raise HTTPException(status_code=403, detail=f"Invalid or expired token")

async def get_user_for_refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail=f"Refresh token not found")
    try:
        payload = security.decode_jwt(refresh_token)
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(status_code=401, detail="Not authenticated")
        user_id = int(payload.get("sub"))
        return await UsersDAO.get_user_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=403, detail=f"Invalid or expired refresh token")