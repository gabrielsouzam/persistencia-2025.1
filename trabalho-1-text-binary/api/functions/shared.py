import csv
import os
from typing import List, Type
from pydantic import BaseModel

def get_csv_path(entity_name: str) -> str:
    return f"data/{entity_name}.csv"

def read_all(entity_name: str, model: Type[BaseModel]) -> List[BaseModel]:
    path = get_csv_path(entity_name)
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [model(**row) for row in reader]

def write_all(entity_name: str, data: List[BaseModel]):
    path = get_csv_path(entity_name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].model_dump().keys())
        writer.writeheader()
        for item in data:
            writer.writerow(item.model_dump())
