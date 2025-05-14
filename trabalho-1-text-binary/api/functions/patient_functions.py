from typing import List
from pydantic import BaseModel
from fastapi import HTTPException
from .logger import logger
from api.models.patient_model import Patient
from api.models.appointment_model import Appointment
from .crud_utils import get_csv_path, read_all, write_all

def append_patient(item: Patient):
    data = read_all("patients", Patient)
    if any(int(existing.id) == int(item.id) for existing in data):
        logger.warning(f"Tentativa de inserção duplicada em patients com id={item.id}")
        raise HTTPException(status_code=400, detail=f"Patient with id={item.id} already exists")
    data.append(item)
    write_all("patients", data)
    logger.info(f"Novo paciente adicionado: {item.model_dump()}")

def update_patient(item_id: int, updated_item: Patient):
    data = read_all("patients", Patient)
    for idx, item in enumerate(data):
        if int(item.id) == item_id:
            data[idx] = updated_item
            write_all("patients", data)
            logger.info(f"Paciente com ID {item_id} atualizado")
            return
    raise HTTPException(status_code=404, detail="Patient not found")

def delete_patient(item_id: int):
    data = read_all("patients", Patient)
    filtered = [item for item in data if int(item.id) != item_id]
    if len(data) == len(filtered):
        raise HTTPException(status_code=404, detail="Patient not found")
    write_all("patients", filtered)
    logger.info(f"Paciente com ID {item_id} removido")

    appointments = read_all("appointments", Appointment)
    remaining = [a for a in appointments if int(a.patient_id) != item_id]
    write_all("appointments", remaining)
    logger.info(f"Agendamentos do paciente {item_id} também removidos")
