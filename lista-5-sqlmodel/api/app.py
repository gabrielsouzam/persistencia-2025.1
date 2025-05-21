from fastapi import FastAPI
from api.functions.init_db import init
from api.routes.main_routes import router as main_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init()

app.include_router(main_router)