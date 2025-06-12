from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from api.models.appointment import Appointment
from api.models.doctor import Doctor, DoctorSpecialtyLink

class SpecialtyBase(BaseModel):
    name: str
    description: str

class SpecialtyCreate(SpecialtyBase):
    pass

class SpecialtyRead(SpecialtyBase):
    id: int

class Specialty(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str

    doctors: List["Doctor"] = Relationship(
        back_populates="specialties",
        link_model=DoctorSpecialtyLink
    )
