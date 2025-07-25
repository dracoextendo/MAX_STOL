import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import main_router

static_path = Path(__file__).parent / "static"
app = FastAPI()
app.include_router(main_router)

app.mount('/static', StaticFiles(directory=static_path), 'static')

if __name__ == "__main__":
    uvicorn.run("main:app")
    