from math import ceil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, logger
from sqlmodel import Session, func, select
from api.models.doctor import Doctor
from api.database.session import get_session
import logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.get("/")
def get_doctors(session: Session = Depends(get_session)):
    return session.exec(select(Doctor)).all()

@router.get("/paginated")
def get_doctors_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total_items = session.scalar(
        select(func.count()).select_from(Doctor)
    ) or 0
    offset = (page - 1) * limit
    items: List[Doctor] = session.exec(
        select(Doctor).offset(offset).limit(limit)
    ).all()
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total_items / limit) if total_items else 0
    }
    
@router.get("/count")
def count_doctors(session: Session = Depends(get_session)):
    total = session.exec(select(Doctor)).all()
    return {"quantidade": len(total)}

@router.get("/filter", response_model=List[Doctor])
def filter_doctors(
    name: Optional[str] = None,
    crm: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Doctor)
    if name:
        query = query.where(Doctor.name.ilike(f"%{name}%"))
    if crm:
        query = query.where(Doctor.crm == crm)

    result = session.exec(query).all()
    return result

@router.get("/{doctor_id}")
def get_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.post("/")
def create_doctor(doctor: Doctor, session: Session = Depends(get_session)):
    session.add(doctor)
    session.commit()
    session.refresh(doctor)
    logger.info(f"Doutor criado: {doctor.name} (id={doctor.id})")
    return doctor

@router.put("/{doctor_id}")
def update_doctor(doctor_id: int, updated: Doctor, session: Session = Depends(get_session)):
    doctor = session.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(doctor, key, value)
    session.commit()
    logger.info(f"Doutor alterado: {doctor.name} (id={doctor.id})")
    return doctor

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, session: Session = Depends(get_session)):
    doctor = session.get(Doctor, doctor_id)
    logger.info(f"Doutor apagado: {doctor.name} (id={doctor.id})")
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    session.delete(doctor)
    session.commit()
    return {"ok": True}


