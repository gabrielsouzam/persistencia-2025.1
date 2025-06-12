from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from api.models.specialty import Specialty
from api.database.session import get_session

router = APIRouter(prefix="/specialties", tags=["Specialties"])

@router.get("/")
def get_specialties(session: Session = Depends(get_session)):
    return session.exec(select(Specialty)).all()

@router.get("/{specialty_id}")
def get_specialty(specialty_id: int, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, specialty_id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    return specialty

@router.post("/")
def create_specialty(specialty: Specialty, session: Session = Depends(get_session)):
    session.add(specialty)
    session.commit()
    session.refresh(specialty)
    return specialty

@router.put("/{specialty_id}")
def update_specialty(specialty_id: int, updated: Specialty, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, specialty_id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(specialty, key, value)
    session.commit()
    return specialty

@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: int, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, specialty_id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    session.delete(specialty)
    session.commit()
    return {"ok": True}

@router.get("/specialties/count")
def count_specialties(session: Session = Depends(get_session)):
    total = session.exec(select(Specialty)).all()
    return {"quantidade": len(total)}

@router.get("/specialties/paginated", response_model=List[Specialty])
def get_specialties_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    result = session.exec(select(Specialty).offset(offset).limit(limit)).all()
    return result

@router.get("/specialties/filter", response_model=List[Specialty])
def filter_specialties(
    name: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Specialty)
    if name:
        query = query.where(Specialty.name.ilike(f"%{name}%"))

    result = session.exec(query).all()
    return result