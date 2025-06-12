from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from api.models.prescription import Prescription
from api.database.session import get_session

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])

@router.get("/")
def get_prescriptions(session: Session = Depends(get_session)):
    return session.exec(select(Prescription)).all()

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
    return prescription

@router.put("/{prescription_id}")
def update_prescription(prescription_id: int, updated: Prescription, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(prescription, key, value)
    session.commit()
    return prescription

@router.delete("/{prescription_id}")
def delete_prescription(prescription_id: int, session: Session = Depends(get_session)):
    prescription = session.get(Prescription, prescription_id)
    if not prescription:
        raise HTTPException(status_code=404, detail="Prescription not found")
    session.delete(prescription)
    session.commit()
    return {"ok": True}

@router.get("/prescriptions/count")
def count_prescriptions(session: Session = Depends(get_session)):
    total = session.exec(select(Prescription)).all()
    return {"quantidade": len(total)}

@router.get("/prescriptions/paginated", response_model=List[Prescription])
def get_prescriptions_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    result = session.exec(select(Prescription).offset(offset).limit(limit)).all()
    return result

@router.get("/prescriptions/filter", response_model=List[Prescription])
def filter_prescriptions(
    appointment_id: Optional[int] = None,
    medicamento: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Prescription)
    if appointment_id:
        query = query.where(Prescription.appointment_id == appointment_id)
    if medicamento:
        query = query.where(Prescription.medicamento.ilike(f"%{medicamento}%"))

    result = session.exec(query).all()
    return result