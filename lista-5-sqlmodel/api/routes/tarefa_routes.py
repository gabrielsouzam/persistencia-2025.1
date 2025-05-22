from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models.models import Tarefa

router = APIRouter()

@router.post("/tarefa/", response_model=Tarefa)
def create_tarefa(tarefa: Tarefa):
    with Session(engine) as session:
        session.add(tarefa)
        session.commit()
        session.refresh(tarefa)
        return tarefa

@router.get("/tarefa/", response_model=list[Tarefa])
def read_tarefas():
    with Session(engine) as session:
        items = session.exec(select(Tarefa)).all()
        return items

@router.get("/tarefa/{item_id}", response_model=Tarefa)
def read_tarefa(item_id: int):
    with Session(engine) as session:
        item = session.get(Tarefa, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="tarefa não encontrado")
        return item

@router.put("/tarefa/{item_id}", response_model=Tarefa)
def update_tarefa(item_id: int, new_data: Tarefa):
    with Session(engine) as session:
        item = session.get(Tarefa, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="tarefa não encontrado")
        for key, value in new_data.dict(exclude_unset=True).items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
        return item

@router.delete("/tarefa/{item_id}")
def delete_tarefa(item_id: int):
    with Session(engine) as session:
        item = session.get(Tarefa, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="tarefa não encontrado")
        session.delete(item)
        session.commit()
        return {"ok": True}
    