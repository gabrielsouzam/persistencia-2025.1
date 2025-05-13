from pydantic import BaseModel

class Doctor(BaseModel):
    id: int
    name: str
    specialty: str
    email: str
    phone: str
    crm: str