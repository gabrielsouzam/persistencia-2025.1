from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models.models import Equipe

router = APIRouter()

@router.post("/equipes/", response_model=Equipe)
def create_equipe(equipe: Equipe):
    with Session(engine) as session:
        session.add(equipe)
        session.commit()
        session.refresh(equipe)
        return equipe

@router.get("/equipes/", response_model=list[Equipe])
def read_equipes():
    with Session(engine) as session:
        equipes = session.exec(select(Equipe)).all()
        return equipes

@router.get("/equipes/{equipe_id}", response_model=Equipe)
def read_equipe(equipe_id: int):
    with Session(engine) as session:
        equipe = session.get(Equipe, equipe_id)
        if not equipe:
            raise HTTPException(status_code=404, detail="Equipe não encontrada")
        return equipe

@router.put("/equipes/{equipe_id}", response_model=Equipe)
def update_equipe(equipe_id: int, new_data: Equipe):
    with Session(engine) as session:
        equipe = session.get(Equipe, equipe_id)
        if not equipe:
            raise HTTPException(status_code=404, detail="Equipe não encontrada")
        equipe.nome = new_data.nome
        equipe.descricao = new_data.descricao
        session.commit()
        session.refresh(equipe)
        return equipe

@router.delete("/equipes/{equipe_id}")
def delete_equipe(equipe_id: int):
    with Session(engine) as session:
        equipe = session.get(Equipe, equipe_id)
        if not equipe:
            raise HTTPException(status_code=404, detail="Equipe não encontrada")
        session.delete(equipe)
        session.commit()
        return {"ok": True}
