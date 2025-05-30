from fastapi import APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from api.models.models import Like
from api.database import engine, get_session

router = APIRouter()
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=Like,
        create_schema=Like,
        update_schema=Like,
        db_model=Like,
        db=get_session,  
        prefix="likes",
        tags=["Likes"]
    ),
    prefix="/likes"
)