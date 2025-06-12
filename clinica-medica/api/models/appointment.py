from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.models.doctor import Doctor
    from api.models.patient import Patient
    from api.models.prescription import Prescription
    
class AppointmentBase(BaseModel):
    doctor_id: int
    patient_id: int
    date: str
    time: str
    status: str

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentRead(AppointmentBase):
    id: int

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    doctor_id: int = Field(foreign_key="doctor.id")
    patient_id: int = Field(foreign_key="patient.id")
    date: str
    time: str
    status: str

    doctor: Optional["Doctor"] = Relationship(back_populates="appointments")
    patient: Optional["Patient"] = Relationship(back_populates="appointments")
    prescriptions: List["Prescription"] = Relationship(back_populates="appointment")