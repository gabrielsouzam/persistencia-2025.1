from typing import Optional, List, TYPE_CHECKING
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

from api.models.specialty import Specialty, SpecialtyRead

if TYPE_CHECKING:
    from api.models.appointment import Appointment
    
    
class DoctorBase(SQLModel):
    name: str
    email: str
    crm: str

class DoctorCreate(DoctorBase):
    specialty_id: Optional[int]

class DoctorRead(DoctorBase):
    id: int
    specialty: Optional["SpecialtyRead"]
    
class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    crm: str

    specialty_id: Optional[int] = Field(default=None, foreign_key="specialty.id")
    specialty: Optional["Specialty"] = Relationship(back_populates="doctors")

    appointments: list["Appointment"] = Relationship(back_populates="doctor")



