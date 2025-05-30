from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models.models import Projeto

router = APIRouter()

@router.post("/projeto/", response_model=Projeto)
def create_projeto(projeto: Projeto):
    with Session(engine) as session:
        session.add(projeto)
        session.commit()
        session.refresh(projeto)
        return projeto

@router.get("/projeto/", response_model=list[Projeto])
def read_projetos():
    with Session(engine) as session:
        items = session.exec(select(Projeto)).all()
        return items

@router.get("/projeto/{item_id}", response_model=Projeto)
def read_projeto(item_id: int):
    with Session(engine) as session:
        item = session.get(Projeto, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="projeto não encontrado")
        return item

@router.put("/projeto/{item_id}", response_model=Projeto)
def update_projeto(item_id: int, new_data: Projeto):
    with Session(engine) as session:
        item = session.get(Projeto, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="projeto não encontrado")
        for key, value in new_data.dict(exclude_unset=True).items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
        return item

@router.delete("/projeto/{item_id}")
def delete_projeto(item_id: int):
    with Session(engine) as session:
        item = session.get(Projeto, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="projeto não encontrado")
        session.delete(item)
        session.commit()
        return {"ok": True}
    