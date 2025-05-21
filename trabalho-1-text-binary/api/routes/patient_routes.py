from fastapi import APIRouter, Query
from typing import Optional
from fastapi.responses import FileResponse
from api.models.patient_model import Patient
from api.functions.shared import read_all
from api.functions.patient_functions import (
    append_patient,
    update_patient,
    delete_patient,
    count_patients,
    zip_patients,
    hash_patients,
    xml_patients,
    filter_patients
)

router = APIRouter()

@router.post("/")
def create(item: Patient):
    append_patient(item)
    return {"message": "Patient created"}

@router.get("/")
def get_all():
    return read_all("patients", Patient)

@router.get("/count")
def count():
    return {"count": count_patients()}

@router.get("/hash")
def hash_csv():
    return {"hash": hash_patients()}

@router.get("/zip")
def download_zip():
    path = zip_patients()
    return FileResponse(path=path, filename="patients.zip", media_type="application/zip")

@router.get("/xml")
def download_xml():
    path = xml_patients()
    return FileResponse(path=path, filename="patients.xml", media_type="application/xml")

@router.get("/filter")
def filter_patient(
    name: Optional[str] = None,
    gender: Optional[str] = None,
    email: Optional[str] = None
):
    filters = {k: v for k, v in {
        "name": name,
        "gender": gender,
        "email": email
    }.items() if v is not None}
    return filter_patients(filters)

@router.put("/{item_id}")
def update(item_id: int, item: Patient):
    update_patient(item_id, item)
    return {"message": "Patient updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    delete_patient(item_id)
    return {"message": "Patient deleted"}
