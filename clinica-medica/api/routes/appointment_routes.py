from math import ceil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select
from api.database.session import get_session
from api.models.appointment import Appointment, AppointmentCreate
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.get("/")
def get_appointments(session: Session = Depends(get_session)):
    return session.exec(select(Appointment)).all()

@router.get("/paginated")
def get_appointments_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total_items = session.scalar(
        select(func.count()).select_from(Appointment)
    ) or 0
    offset = (page - 1) * limit
    items: List[Appointment] = session.exec(
        select(Appointment).offset(offset).limit(limit)
    ).all()
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total_items / limit) if total_items else 0
    }

@router.get("/count")
def count_appointments(session: Session = Depends(get_session)):
    total = session.exec(select(Appointment)).all()
    return {"quantidade": len(total)}

@router.get("/filter", response_model=List[Appointment])
def filter_appointments(
    patient_id: Optional[int] = None,
    doctor_id: Optional[int] = None,
    session: Session = Depends(get_session)
):
    query = select(Appointment)
    if patient_id:
        query = query.where(Appointment.patient_id == patient_id)
    if doctor_id:
        query = query.where(Appointment.doctor_id == doctor_id)

    result = session.exec(query).all()
    return result

@router.get("/{appointment_id}")
def get_appointment(appointment_id: int, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return appointment

@router.post("/")
def create_appointment(appointment: AppointmentCreate, session: Session = Depends(get_session)):
    newAppointment = Appointment.from_orm(appointment)
    session.add(newAppointment)
    session.commit()
    session.refresh(newAppointment)
    logger.info(f"Paciente criado: {newAppointment.date} (id={newAppointment.id})")
    
    return newAppointment

@router.put("/{appointment_id}")
def update_appointment(appointment_id: int, updated: Appointment, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(appointment, key, value)
    session.commit()
    return appointment

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, session: Session = Depends(get_session)):
    appointment = session.get(Appointment, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    session.delete(appointment)
    session.commit()
    return {"ok": True}





