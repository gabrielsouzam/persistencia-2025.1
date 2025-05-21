from typing import List, Dict, Any
from fastapi import HTTPException
from api.models.doctor_model import Doctor
from api.models.appointment_model import Appointment
from .shared import get_csv_path, read_all, write_all
import hashlib, zipfile, os, csv, xml.etree.ElementTree as ET

ENTITY = "doctors"

def append_doctor(item: Doctor):
    data = read_all(ENTITY, Doctor)
    if any(int(existing.id) == int(item.id) for existing in data):
        raise HTTPException(status_code=400, detail="Doctor with this ID already exists")
    data.append(item)
    write_all(ENTITY, data)

def update_doctor(item_id: int, item: Doctor):
    data = read_all(ENTITY, Doctor)
    for idx, doctor in enumerate(data):
        if int(doctor.id) == item_id:
            data[idx] = item
            write_all(ENTITY, data)
            return
    raise HTTPException(status_code=404, detail="Doctor not found")

def delete_doctor(item_id: int):
    data = read_all(ENTITY, Doctor)
    filtered = [item for item in data if int(item.id) != item_id]
    if len(data) == len(filtered):
        raise HTTPException(status_code=404, detail="Doctor not found")
    write_all(ENTITY, filtered)

    appointments = read_all("appointments", Appointment)
    updated_appointments = [a for a in appointments if int(a.doctor_id) != item_id]
    write_all("appointments", updated_appointments)

def count_doctors() -> int:
    return len(read_all(ENTITY, Doctor))

def zip_doctors() -> str:
    path = get_csv_path(ENTITY)
    zip_path = f"data/{ENTITY}.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(path, arcname=os.path.basename(path))
    return zip_path

def hash_doctors() -> str:
    path = get_csv_path(ENTITY)
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def xml_doctors() -> str:
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

def filter_doctors(filters: Dict[str, Any]) -> List[Doctor]:
    data = read_all(ENTITY, Doctor)
    return [item for item in data if all(str(getattr(item, k, "")).lower() == str(v).lower() for k, v in filters.items())]
