from typing import List
from pydantic import BaseModel
from fastapi import HTTPException
from .logger import logger
from api.models.doctor_model import Doctor
from api.models.appointment_model import Appointment
from .crud_utils import get_csv_path, read_all, write_all

def append_doctor(item: Doctor):
    data = read_all("doctors", Doctor)
    if any(int(existing.id) == int(item.id) for existing in data):
        logger.warning(f"Tentativa de inserção duplicada em doctors com id={item.id}")
        raise HTTPException(status_code=400, detail=f"Doctor with id={item.id} already exists")
    data.append(item)
    write_all("doctors", data)
    logger.info(f"Novo médico adicionado: {item.model_dump()}")

def update_doctor(item_id: int, updated_item: Doctor):
    data = read_all("doctors", Doctor)
    for idx, item in enumerate(data):
        if int(item.id) == item_id:
            data[idx] = updated_item
            write_all("doctors", data)
            logger.info(f"Médico com ID {item_id} atualizado")
            return
    raise HTTPException(status_code=404, detail="Doctor not found")

def delete_doctor(item_id: int):
    data = read_all("doctors", Doctor)
    filtered = [item for item in data if int(item.id) != item_id]
    if len(data) == len(filtered):
        raise HTTPException(status_code=404, detail="Doctor not found")
    write_all("doctors", filtered)
    logger.info(f"Médico com ID {item_id} removido")

    appointments = read_all("appointments", Appointment)
    remaining = [a for a in appointments if int(a.doctor_id) != item_id]
    write_all("appointments", remaining)
    logger.info(f"Agendamentos do médico {item_id} também removidos")
