from fastapi import APIRouter
from api.models.patient_model import Patient
from api.functions import crud_utils as crud
from fastapi.responses import FileResponse
from typing import Optional

router = APIRouter()
ENTITY = "patients"

@router.get("/filter")
def filter_patients(
    name: Optional[str] = None,
    gender: Optional[str] = None,
    email: Optional[str] = None
):
    filters = {k: v for k, v in {
        "name": name,
        "gender": gender,
        "email": email
    }.items() if v is not None}

    return crud.filter_entities(ENTITY, Patient, filters)


@router.post("/")
def create(item: Patient):
    crud.append_entity(ENTITY, item)
    return {"message": "Patient created"}

@router.get("/")
def get_all():
    return crud.read_all(ENTITY, Patient)

@router.get("/count")
def count():
    return {"count": crud.count_entities(ENTITY)}

@router.get("/hash")
def hash_csv():
    return {"hash_sha256": crud.get_csv_hash(ENTITY)}

@router.get("/zip")
def download_zip():
    zip_path = crud.zip_csv(ENTITY)
    return FileResponse(
        path=zip_path,
        filename=f"{ENTITY}.zip",
        media_type="application/zip"
    )

@router.get("/xml")
def download_xml():
    xml_path = crud.csv_to_xml(ENTITY)
    return FileResponse(
        path=xml_path,
        filename=f"{ENTITY}.xml",
        media_type="application/xml"
    )

@router.put("/{item_id}")
def update(item_id: int, item: Patient):
    crud.update_entity(ENTITY, item_id, item)
    return {"message": "Patient updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    crud.delete_entity(ENTITY, item_id, Patient)
    return {"message": "Patient deleted"}