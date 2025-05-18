from fastapi import Request, HTTPException
from src import security

async def access_token_validation(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        security.decode_jwt(token)
    except Exception:
        raise HTTPException(status_code=401, detail=f"Invalid or expired token")