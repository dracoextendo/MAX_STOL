import sys
from pathlib import Path

from authx.exceptions import MissingTokenError

sys.path.append(str(Path(__file__).parent.parent))
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from src.api import main_router

app = FastAPI()

@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Unauthorized"},
    )
app.include_router(main_router)
app.mount('/static', StaticFiles(directory='./static'), 'static')



if __name__ == "__main__":
    uvicorn.run("main:app")
    