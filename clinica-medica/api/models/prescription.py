from __future__ import annotations
from typing import Optional
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from api.models.appointment import Appointment

class PrescriptionBase(BaseModel):
    appointment_id: int
    medication: str
    dosage: str
    instructions: str

class PrescriptionCreate(PrescriptionBase):
    pass

class PrescriptionRead(PrescriptionBase):
    id: int

class Prescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    appointment_id: int = Field(foreign_key="appointment.id")
    medication: str
    dosage: str
    instructions: str

    appointment: Optional["Appointment"] = Relationship(back_populates="prescriptions")

