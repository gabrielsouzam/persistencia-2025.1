from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, func, select
from api.database.session import get_session
from api.models.patient import Patient, PatientCreate, PatientRead
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/")
def get_all_patient(session: Session = Depends(get_session)):
    return session.exec(select(Patient)).all()

@router.post("/", response_model=PatientRead)
def create_patient(paciente: PatientCreate, session: Session = Depends(get_session)):
    novo_paciente = Patient(**paciente.dict())
    session.add(novo_paciente)
    session.commit()
    session.refresh(novo_paciente)
    logger.info(f"Paciente criado: {novo_paciente.name} (id={novo_paciente.id})")
    return novo_paciente

@router.get("/paginated")
def get_patients_paginated(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    total_items = session.scalar(
        select(func.count()).select_from(Patient)
    ) or 0
    offset = (page - 1) * limit
    items: List[Patient] = session.exec(
        select(Patient).offset(offset).limit(limit)
    ).all()
    return {
        "items": items,
        "total_items": total_items,
        "page": page,
        "limit": limit,
        "total_pages": ceil(total_items / limit) if total_items else 0
    }

@router.get("/count")
def count_patient(session: Session = Depends(get_session)):
    total = session.exec(select(Patient)).all()
    return {"quantidade": len(total)}

@router.get("/filter", response_model=List[Patient])
def filter_patients(
    name: Optional[str] = None,
    email: Optional[str] = None,
    session: Session = Depends(get_session)
):
    query = select(Patient)
    if name:
        query = query.where(Patient.name.ilike(f"%{name}%"))
    if email:
        query = query.where(Patient.email.ilike(f"%{email}%"))

    results = session.exec(query).all()
    return results

@router.get("/{paciente_id}", response_model=PatientRead)
def get_patient_by_id(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Patient, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@router.put("/{paciente_id}", response_model=PatientRead)
def update_patient(paciente_id: int, dados: PatientCreate, session: Session = Depends(get_session)):
    paciente = session.get(Patient, paciente_id)
    if not paciente:
        logger.warning(f"Update falhou: Paciente não encontrado (id={paciente_id})")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    for key, value in dados.dict().items():
        setattr(paciente, key, value)
    session.commit()
    session.refresh(paciente)
    logger.info(f"Paciente atualizado: {paciente.name} (id={paciente.id})")
    return paciente

@router.delete("/{paciente_id}")
def delete_patient(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Patient, paciente_id)
    if not paciente:
        logger.warning(f"Tentativa de deletar paciente inexistente (id={paciente_id})")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    session.delete(paciente)
    session.commit()
    logger.info(f"Paciente deletado: {paciente.name} (id={paciente.id})")
    return {"ok": True, "message": "Paciente deletado"}

