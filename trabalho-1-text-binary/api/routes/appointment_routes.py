from fastapi import APIRouter, Query
from typing import Optional
from fastapi.responses import FileResponse
from api.models.appointment_model import Appointment
from api.functions.shared import read_all
from api.functions.appointment_functions import (
    append_appointment,
    update_appointment,
    delete_appointment,
    count_appointments,
    zip_appointments,
    hash_appointments,
    xml_appointments,
    filter_appointments
)

router = APIRouter()

@router.post("/")
def create(item: Appointment):
    append_appointment(item)
    return {"message": "Appointment created"}

@router.get("/")
def get_all():
    return read_all("appointments", Appointment)

@router.get("/count")
def count():
    return {"count": count_appointments()}

@router.get("/hash")
def hash_csv():
    return {"hash": hash_appointments()}

@router.get("/zip")
def download_zip():
    path = zip_appointments()
    return FileResponse(path=path, filename="appointments.zip", media_type="application/zip")

@router.get("/xml")
def download_xml():
    path = xml_appointments()
    return FileResponse(path=path, filename="appointments.xml", media_type="application/xml")

@router.get("/filter")
def filter_appointment(
    doctor_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    status: Optional[str] = None
):
    filters = {k: v for k, v in {
        "doctor_id": doctor_id,
        "patient_id": patient_id,
        "status": status
    }.items() if v is not None}
    return filter_appointments(filters)

@router.put("/{item_id}")
def update(item_id: int, item: Appointment):
    update_appointment(item_id, item)
    return {"message": "Appointment updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    delete_appointment(item_id)
    return {"message": "Appointment deleted"}
