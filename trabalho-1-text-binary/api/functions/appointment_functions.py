from typing import List, Dict, Any
from fastapi import HTTPException
from api.models.appointment_model import Appointment
from api.models.doctor_model import Doctor
from api.models.patient_model import Patient
from .shared import get_csv_path, read_all, write_all
import hashlib, zipfile, os, csv, xml.etree.ElementTree as ET

ENTITY = "appointments"

def validate_appointment(app: Appointment) -> bool:
    doctors = read_all("doctors", Doctor)
    patients = read_all("patients", Patient)
    if not any(int(d.id) == app.doctor_id for d in doctors):
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not any(int(p.id) == app.patient_id for p in patients):
        raise HTTPException(status_code=404, detail="Patient not found")
    return True

def append_appointment(item: Appointment):
    data = read_all(ENTITY, Appointment)
    if any(int(existing.id) == int(item.id) for existing in data):
        raise HTTPException(status_code=400, detail="Appointment with this ID already exists")
    validate_appointment(item)
    data.append(item)
    write_all(ENTITY, data)

def update_appointment(item_id: int, item: Appointment):
    data = read_all(ENTITY, Appointment)
    for idx, appt in enumerate(data):
        if int(appt.id) == item_id:
            data[idx] = item
            write_all(ENTITY, data)
            return
    raise HTTPException(status_code=404, detail="Appointment not found")

def delete_appointment(item_id: int):
    data = read_all(ENTITY, Appointment)
    filtered = [item for item in data if int(item.id) != item_id]
    if len(data) == len(filtered):
        raise HTTPException(status_code=404, detail="Appointment not found")
    write_all(ENTITY, filtered)

def count_appointments() -> int:
    return len(read_all(ENTITY, Appointment))

def zip_appointments() -> str:
    path = get_csv_path(ENTITY)
    zip_path = f"data/{ENTITY}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(path, arcname=os.path.basename(path))
    return zip_path

def hash_appointments() -> str:
    path = get_csv_path(ENTITY)
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def xml_appointments() -> str:
    path = get_csv_path(ENTITY)
    root = ET.Element(ENTITY)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = ET.SubElement(root, "item")
            for k, v in row.items():
                ET.SubElement(item, k).text = v
    xml_path = f"data/{ENTITY}.xml"
    ET.ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)
    return xml_path

def filter_appointments(filters: Dict[str, Any]) -> List[Appointment]:
    data = read_all(ENTITY, Appointment)
    return [item for item in data if all(str(getattr(item, k, "")).lower() == str(v).lower() for k, v in filters.items())]
