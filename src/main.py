import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api import main_router

app = FastAPI()
app.include_router(main_router)
app.mount('/static', StaticFiles(directory='./static'), 'static')



if __name__ == "__main__":
    uvicorn.run("main:app")