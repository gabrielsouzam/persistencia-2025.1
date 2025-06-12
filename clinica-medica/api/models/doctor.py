from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from api.models.specialty import SpecialtyRead

if TYPE_CHECKING:
    from api.models.appointment import Appointment
    from api.models.specialty import Specialty
    
class DoctorBase(BaseModel):
    name: str
    email: str
    crm: str

class DoctorCreate(DoctorBase):
    specialty_ids: Optional[List[int]] = []

class DoctorRead(DoctorBase):
    id: int
    specialties: Optional[List["SpecialtyRead"]] = []
    
class DoctorSpecialtyLink(SQLModel, table=True):
    doctor_id: Optional[int] = Field(default=None, foreign_key="doctor.id", primary_key=True)
    specialty_id: Optional[int] = Field(default=None, foreign_key="specialty.id", primary_key=True)

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    crm: str

    specialties: List[Specialty] = Relationship(
        back_populates="doctors",
        link_model=DoctorSpecialtyLink
    )

    appointments: List["Appointment"] = Relationship(back_populates="doctor")



