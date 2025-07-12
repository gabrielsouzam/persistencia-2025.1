from math import ceil
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select
from api.models.prescription import Prescription
from api.database.session import get_session
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.get("/")
def get_prescriptions(session: Session = Depends(get_session)):
    return session.exec(select(Prescription)).all()

@router.get("/paginated")
def get_prescriptions_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total_items = session.scalar(
        select(func.count()).select_from(Prescription)
    ) or 0
    offset = (page - 1) * limit
    items: List[Prescription] = session.exec(
        select(Prescription).offset(offset).limit(limit)
    ).all()
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total_items / limit) if total_items else 0
    }
    
@router.get("/count")
def count_prescriptions(session: Session = Depends(get_session)):
    total = session.exec(select(Prescription)).all()
    return {"quantidade": len(total)}

@router.get("/filter", response_model=List[Prescription])
def filter_prescriptions(
    appointment_id: Optional[int] = None,
    medicamento: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Prescription)
    if appointment_id:
        query = query.where(Prescription.appointment_id == appointment_id)
    if medicamento:
        query = query.where(Prescription.medication.ilike(f"%{medicamento}%"))

    result = session.exec(query).all()
    return result

@router.get("/{prescription_id}")
def get_prescription(prescription_id: int, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return prescription

@router.post("/")
def create_prescription(prescription: Prescription, session: Session = Depends(get_session)):
    session.add(prescription)
    session.commit()
    session.refresh(prescription)
    logger.info(f"Prescrição criada: {prescription.instructions} (id={prescription.id})")
    return prescription

@router.put("/{prescription_id}")
def update_prescription(prescription_id: int, updated: Prescription, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(prescription, key, value)
    session.commit()
    logger.info(f"Prescrição alterada: {prescription.instructions} (id={prescription.id})")
    return prescription

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    session.delete(prescription)
    session.commit()
    logger.info(f"Prescrição apagada: {prescription.instructions} (id={prescription.id})")
    return {"ok": True}




