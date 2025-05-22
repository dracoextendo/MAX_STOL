import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware
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

if __name__ == "__main__":
    uvicorn.run("main:app")
    