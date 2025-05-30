from fastapi import APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from api.models.models import Comment
from api.database import engine, get_session

router = APIRouter()
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=Comment,
        create_schema=Comment,
        update_schema=Comment,
        db_model=Comment,
        db=get_session,  
        prefix="comments",
        tags=["Comments"]
    ),
    prefix="/comments"
)