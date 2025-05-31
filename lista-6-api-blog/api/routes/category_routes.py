from fastapi import APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from api.models.models import Category, CategoryRead
from api.database import engine, get_session

router = APIRouter()
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=CategoryRead,
        create_schema=Category,
        update_schema=Category,
        db_model=Category,
        db=get_session,  
        prefix="categories",
        tags=["Categories"]
    ),
    prefix="/categories"
)