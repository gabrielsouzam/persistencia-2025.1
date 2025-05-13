from pydantic import BaseModel

class Patient(BaseModel):
    id: int
    name: str
    birthdate: str
    gender: str
    email: str
    phone: str