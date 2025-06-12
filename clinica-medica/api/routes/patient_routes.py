from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from api.database.session import get_session
from api.models.patient import Patient, PatientCreate, PatientRead
from typing import List, Optional
import logging

router = APIRouter(prefix="/patients", tags=["Patients"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=PatientRead)
def criar_paciente(paciente: PatientCreate, session: Session = Depends(get_session)):
    novo_paciente = Patient.from_orm(paciente)
    session.add(novo_paciente)
    session.commit()
    session.refresh(novo_paciente)
    logger.info(f"Paciente criado: {novo_paciente.name} (id={novo_paciente.id})")
    return novo_paciente

@router.get("/", response_model=List[PatientRead])
def listar_pacientes(page: int = 1, limit: int = 10, session: Session = Depends(get_session)):
    offset = (page - 1) * limit
    pacientes = session.exec(select(Patient).offset(offset).limit(limit)).all()
    return pacientes

@router.get("/contagem")
def contar_pacientes(session: Session = Depends(get_session)):
    total = session.exec(select(Patient)).all()
    return {"quantidade": len(total)}

@router.get("/filtrar", response_model=List[PatientRead])
def filtrar_pacientes(
    nome: Optional[str] = None,
    email: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    session: Session = Depends(get_session)
):
    offset = (page - 1) * limit
    query = select(Patient)
    if nome:
        query = query.where(Patient.name.ilike(f"%{nome}%"))
    if email:
        query = query.where(Patient.email.ilike(f"%{email}%"))
    pacientes = session.exec(query.offset(offset).limit(limit)).all()
    return pacientes

@router.get("/{paciente_id}", response_model=PatientRead)
def buscar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Patient, paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente

@router.put("/{paciente_id}", response_model=PatientRead)
def atualizar_paciente(paciente_id: int, dados: PatientCreate, session: Session = Depends(get_session)):
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
def deletar_paciente(paciente_id: int, session: Session = Depends(get_session)):
    paciente = session.get(Patient, paciente_id)
    if not paciente:
        logger.warning(f"Tentativa de deletar paciente inexistente (id={paciente_id})")
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    session.delete(paciente)
    session.commit()
    logger.info(f"Paciente deletado: {paciente.name} (id={paciente.id})")
    return {"ok": True, "message": "Paciente deletado"}