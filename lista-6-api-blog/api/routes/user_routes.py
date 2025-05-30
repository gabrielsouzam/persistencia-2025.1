from fastapi import APIRouter
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from api.models.models import User
from api.database import engine, get_session

router = APIRouter()
router.include_router(
    SQLAlchemyCRUDRouter(
        schema=User,
        create_schema=User,
        update_schema=User,
        db_model=User,
        db=get_session,  
        prefix="users",
        tags=["Users"]
    ),
    prefix="/users"
)