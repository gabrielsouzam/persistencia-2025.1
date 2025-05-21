from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API ORM com SQLModel funcionando!"}