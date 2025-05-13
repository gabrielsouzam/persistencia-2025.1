from fastapi import APIRouter
from api.models.doctor_model import Doctor
from api.functions import crud_utils as crud
from fastapi.responses import FileResponse

router = APIRouter()
ENTITY = "doctors"

@router.post("/")
def create(item: Doctor):
    crud.append_entity(ENTITY, item)
    return {"message": "Doctor created"}

@router.get("/")
def get_all():
    return crud.read_all(ENTITY, Doctor)

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
def update(item_id: int, item: Doctor):
    crud.update_entity(ENTITY, item_id, item)
    return {"message": "Doctor updated"}

@router.delete("/{item_id}")
def delete(item_id: int):
    crud.delete_entity(ENTITY, item_id, Doctor)
    return {"message": "Doctor deleted"}