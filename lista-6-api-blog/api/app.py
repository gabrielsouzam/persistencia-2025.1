from fastapi import FastAPI
from api.functions.init_db import init_db
from api.routes.user_routes import router as user_router
from api.routes.category_routes import router as category_router
from api.routes.post_routes import router as post_router
from api.routes.comment_routes import router as comment_router
from api.routes.like_routes import router as like_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)