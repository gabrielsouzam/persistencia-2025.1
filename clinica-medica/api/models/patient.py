from typing import List, Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from api.models.appointment import Appointment

class PatientBase(SQLModel):
    name: str
    email: str
    cpf: str

class PatientCreate(PatientBase, table=False):
    pass

class PatientRead(PatientBase):
    id: int

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    cpf: str

    appointments: list["Appointment"] = Relationship(back_populates="patient")