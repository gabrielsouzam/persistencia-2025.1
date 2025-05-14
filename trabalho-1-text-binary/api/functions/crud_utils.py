import csv, os, hashlib, zipfile
from typing import List, Type
from pydantic import BaseModel
from fastapi import HTTPException
import xml.etree.ElementTree as ET
from api.models.appointment_model import Appointment
from api.models.doctor_model import Doctor
from api.models.patient_model import Patient
import os
import xml.etree.ElementTree as ET
import csv
from .logger import logger

def get_csv_path(entity_name: str) -> str:
    return f"data/{entity_name}.csv"

def read_all(entity_name: str, model: Type[BaseModel]) -> List[BaseModel]:
    path = get_csv_path(entity_name)
    if not os.path.exists(path):
        logger.warning(f"Arquivo CSV não encontrado para {entity_name}")
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [model(**row) for row in reader]
        logger.info(f"{len(data)} registros lidos de {entity_name}")
        return data

def write_all(entity_name: str, data: List[BaseModel]):
    path = get_csv_path(entity_name)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].model_dump().keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item.model_dump())
        logger.info(f"{len(data)} registros escritos em {entity_name}")
            
def validate_appointment(appointment: Appointment) -> bool:
    doctor = read_all("doctors", Doctor)
    patient = read_all("patients", Patient)
    doctor_exists = False
    patient_exists = False
    for d in doctor:
        if int(d.id) == int(appointment.doctor_id):
            doctor_exists = True
            break
    for p in patient:
        if int(p.id) == int(appointment.patient_id):
            patient_exists = True
            break
    if not doctor_exists:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if not patient_exists:
        raise HTTPException(status_code=404, detail="Patient not found")
    return True

def append_entity(entity_name: str, item: BaseModel):
    data = read_all(entity_name, type(item))
    
    if any(int(existing.id) == int(item.id) for existing in data):
        logger.warning(f"Tentativa de inserção duplicada em {entity_name} com id={item.id}")
        raise HTTPException(status_code=400, detail=f"Item with id={item.id} already exists")
    
    if entity_name == 'appointments':
        if not validate_appointment(item):
            logger.error("Agendamento inválido")
            raise HTTPException(status_code=400, detail="Invalid appointment data")
    data.append(item)
    write_all(entity_name, data)
    logger.info(f"Novo item adicionado em {entity_name}: {item.model_dump()}")

def update_entity(entity_name: str, item_id: int, updated_item: BaseModel):
    data = read_all(entity_name, type(updated_item))
    for idx, item in enumerate(data):
        if int(item.id) == item_id:
            data[idx] = updated_item
            write_all(entity_name, data)
            logger.info(f"Item com ID {item_id} atualizado em {entity_name}")
            return
    logger.error(f"Item com ID {item_id} não encontrado para atualização em {entity_name}")
    raise HTTPException(status_code=404, detail="Item not found")

def delete_entity(entity_name: str, item_id: int, model: Type[BaseModel]):
    data = read_all(entity_name, model)
    filtered = [item for item in data if int(item.id) != item_id]

    if len(data) == len(filtered):
        logger.warning(f"Tentativa de excluir item inexistente com ID {item_id} em {entity_name}")
        raise HTTPException(status_code=404, detail="Item not found")

    write_all(entity_name, filtered)
    logger.info(f"Item com ID {item_id} removido de {entity_name}")

    if entity_name in ['doctors', 'patients']:
        appointments = read_all('appointments', Appointment)
        remaining = [
            item for item in appointments 
            if (int(item.doctor_id) != item_id if entity_name == 'doctors' else int(item.patient_id) != item_id)
        ]
        write_all('appointments', remaining)
        logger.info(f"Agendamentos relacionados a {entity_name} ID {item_id} também foram removidos")
      
def count_entities(entity_name: str) -> int:
    path = get_csv_path(entity_name)
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f) - 1

def zip_csv(entity_name: str) -> str:
    import os, zipfile
    path = get_csv_path(entity_name)
    zip_path = f"data/{entity_name}.zip"

    os.makedirs("data", exist_ok=True)

    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(path, arcname=os.path.basename(path))

    return zip_path


def get_csv_hash(entity_name: str) -> str:
    path = get_csv_path(entity_name)
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(4096), b""):
            sha256.update(block)
    return sha256.hexdigest()

def csv_to_xml(entity_name: str) -> str:
    path = get_csv_path(entity_name)
    tree_root = ET.Element(entity_name)

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item_elem = ET.SubElement(tree_root, "item")
            for key, value in row.items():
                child = ET.SubElement(item_elem, key)
                child.text = value

    os.makedirs("data", exist_ok=True)
    xml_path = f"data/{entity_name}.xml"
    ET.ElementTree(tree_root).write(xml_path, encoding="utf-8", xml_declaration=True)

    return xml_path
