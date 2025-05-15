import sys
from pathlib import Path
from authx.exceptions import MissingTokenError
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(str(Path(__file__).parent.parent))
app = FastAPI()

app.include_router(main_router)

app.mount('/static', StaticFiles(directory='./static'), 'static')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://desk.mafioznik.ru/", "http://127.0.0.1:8000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(MissingTokenError)
async def missing_token_exception_handler(request: Request, exc: MissingTokenError):
    return JSONResponse(
        status_code=401,
        content={"detail": "Unauthorized"},
    )

if __name__ == "__main__":
    uvicorn.run("main:app")
    