from math import ceil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select
from api.models.specialty import Specialty
from api.database.session import get_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/specialties", tags=["Specialties"])

@router.get("/")
def get_specialties(session: Session = Depends(get_session)):
    return session.exec(select(Specialty)).all()

@router.get("/paginated")
def get_specialties_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total_items = session.scalar(
        select(func.count()).select_from(Specialty)
    ) or 0
    offset = (page - 1) * limit
    items: List[Specialty] = session.exec(
        select(Specialty).offset(offset).limit(limit)
    ).all()
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total_items / limit) if total_items else 0
    }
    
@router.get("/count")
def count_specialties(session: Session = Depends(get_session)):
    total = session.exec(select(Specialty)).all()
    return {"quantidade": len(total)}

@router.get("/filter", response_model=List[Specialty])
def filter_specialties(
    name: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Specialty)
    if name:
        query = query.where(Specialty.name.ilike(f"%{name}%"))

    result = session.exec(query).all()
    return result

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
    logger.info(f"Especialidade criada: {Specialty.description} (id={Specialty.id})")
    return specialty

@router.put("/{specialty_id}")
def update_specialty(specialty_id: int, updated: Specialty, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, specialty_id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(specialty, key, value)
    session.commit()
    logger.info(f"Especialidade criada: {Specialty.description} (id={Specialty.id})")
    return specialty

@router.delete("/{specialty_id}")
def delete_specialty(specialty_id: int, session: Session = Depends(get_session)):
    specialty = session.get(Specialty, specialty_id)
    if not specialty:
        raise HTTPException(status_code=404, detail="Specialty not found")
    session.delete(specialty)
    session.commit()
    logger.info(f"Especialidade apagada: {Specialty.description} (id={Specialty.id})")
    return {"ok": True}



