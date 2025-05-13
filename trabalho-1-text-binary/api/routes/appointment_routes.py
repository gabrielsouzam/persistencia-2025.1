from fastapi import APIRouter
from api.models.appointment_model import Appointment
from api.functions import crud_utils as crud
from fastapi.responses import FileResponse

router = APIRouter()
ENTITY = "appointments"

@router.post("/")
def create(item: Appointment):
    crud.append_entity(ENTITY, item)
    return {"message": "Appointment created"}

@router.get("/")
def get_all():
    return crud.read_all(ENTITY, Appointment)

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

from fastapi.responses import FileResponse

@router.get("/xml")
def download_xml():
    xml_path = crud.csv_to_xml(ENTITY)
    return FileResponse(
        path=xml_path,
        filename=f"{ENTITY}.xml",
        media_type="application/xml"
    )

@router.put("/{item_id}")
def update(item_id: int, item: Appointment):
    crud.update_entity(ENTITY, item_id, item)
    return {"message": "Appointment updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    crud.delete_entity(ENTITY, item_id, Appointment)
    return {"message": "Appointment deleted"}