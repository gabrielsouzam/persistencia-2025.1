from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from ..database import engine
from ..models.models import Membro

router = APIRouter()

@router.post("/membro/", response_model=Membro)
def create_membro(membro: Membro):
    with Session(engine) as session:
        session.add(membro)
        session.commit()
        session.refresh(membro)
        return membro

@router.get("/membro/", response_model=list[Membro])
def read_membros():
    with Session(engine) as session:
        items = session.exec(select(Membro)).all()
        return items

@router.get("/membro/{item_id}", response_model=Membro)
def read_membro(item_id: int):
    with Session(engine) as session:
        item = session.get(Membro, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Membro não encontrado")
        return item

@router.put("/membro/{item_id}", response_model=Membro)
def update_membro(item_id: int, new_data: Membro):
    with Session(engine) as session:
        item = session.get(Membro, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Membro não encontrado")
        for key, value in new_data.dict(exclude_unset=True).items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
        return item

@router.delete("/membro/{item_id}")
def delete_membro(item_id: int):
    with Session(engine) as session:
        item = session.get(Membro, item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Membro não encontrado")
        session.delete(item)
        session.commit()
        return {"ok": True}
    