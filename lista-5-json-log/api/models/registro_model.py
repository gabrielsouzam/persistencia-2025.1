from pydantic import BaseModel
from typing import Optional

class Registro(BaseModel):
    id: int
    name: str
    age: Optional[int]