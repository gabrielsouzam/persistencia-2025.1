from pydantic import BaseModel
from fastapi import HTTPException
from api.models.appointment_model import Appointment
from api.models.doctor_model import Doctor
from api.models.patient_model import Patient
from .logger import logger
from .crud_utils import get_csv_path, read_all, write_all

def validate_appointment(appointment: Appointment) -> bool:
    doctors = read_all("doctors", Doctor)
    patients = read_all("patients", Patient)
    if not any(int(d.id) == appointment.doctor_id for d in doctors):
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not any(int(p.id) == appointment.patient_id for p in patients):
        raise HTTPException(status_code=404, detail="Patient not found")
    return True

def append_appointment(item: Appointment):
    data = read_all("appointments", Appointment)
    if any(int(existing.id) == int(item.id) for existing in data):
        logger.warning(f"Tentativa de inserção duplicada em appointments com id={item.id}")
        raise HTTPException(status_code=400, detail=f"Appointment with id={item.id} already exists")
    if not validate_appointment(item):
        raise HTTPException(status_code=400, detail="Invalid appointment")
    data.append(item)
    write_all("appointments", data)
    logger.info(f"Novo agendamento adicionado: {item.model_dump()}")

def update_appointment(item_id: int, updated_item: Appointment):
    data = read_all("appointments", Appointment)
    for idx, item in enumerate(data):
        if int(item.id) == item_id:
            data[idx] = updated_item
            write_all("appointments", data)
            logger.info(f"Agendamento com ID {item_id} atualizado")
            return
    raise HTTPException(status_code=404, detail="Appointment not found")

def delete_appointment(item_id: int):
    data = read_all("appointments", Appointment)
    filtered = [item for item in data if int(item.id) != item_id]
    if len(data) == len(filtered):
        raise HTTPException(status_code=404, detail="Appointment not found")
    write_all("appointments", filtered)
    logger.info(f"Agendamento com ID {item_id} removido")
