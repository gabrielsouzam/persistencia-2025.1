from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from api.models.doctor import Doctor

class SpecialtyBase(SQLModel):
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

    doctors: list["Doctor"] = Relationship(back_populates="specialty")
