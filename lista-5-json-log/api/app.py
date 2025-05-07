from fastapi import FastAPI
from api.routes import processa_routes

app = FastAPI()
app.include_router(processa_routes.router)