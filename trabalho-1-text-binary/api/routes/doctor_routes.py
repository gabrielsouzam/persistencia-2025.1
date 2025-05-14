from fastapi import APIRouter, Query
from typing import Optional
from fastapi.responses import FileResponse
from api.models.doctor_model import Doctor
from api.functions.shared import read_all
from api.functions.doctor_functions import (
    append_doctor,
    update_doctor,
    delete_doctor,
    count_doctors,
    zip_doctors,
    hash_doctors,
    xml_doctors,
    filter_doctors
)

router = APIRouter()

@router.post("/")
def create(item: Doctor):
    append_doctor(item)
    return {"message": "Doctor created"}

@router.get("/")
def get_all():
    return read_all("doctors", Doctor)

@router.get("/count")
def count():
    return {"count": count_doctors()}

@router.get("/hash")
def hash_csv():
    return {"hash": hash_doctors()}

@router.get("/zip")
def download_zip():
    path = zip_doctors()
    return FileResponse(path=path, filename="doctors.zip", media_type="application/zip")

@router.get("/xml")
def download_xml():
    path = xml_doctors()
    return FileResponse(path=path, filename="doctors.xml", media_type="application/xml")

@router.get("/filter")
def filter_doctor(
    name: Optional[str] = None,
    specialty: Optional[str] = None,
    crm: Optional[str] = None
):
    filters = {k: v for k, v in {
        "name": name,
        "specialty": specialty,
        "crm": crm
    }.items() if v is not None}
    return filter_doctors(filters)

@router.put("/{item_id}")
def update(item_id: int, item: Doctor):
    update_doctor(item_id, item)
    return {"message": "Doctor updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    delete_doctor(item_id)
    return {"message": "Doctor deleted"}
