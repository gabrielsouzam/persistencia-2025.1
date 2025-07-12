from typing import List
from fastapi import APIRouter, HTTPException
from database import professores_collection
from bson import ObejctId
from models import ProfessorCreate, ProfessorOut

router = APIRouter(prefix="/professores")

@router.post("/", response_model=ProfessorOut)
async def criar_professor(professor: ProfessorCreate):
  prof_dict = professor.model_dump(exclude_unset=True)
  
  result = await professores_collection.insert_one(prof_dict)
  created = await professores_collection.find_one(
    {
      "_id": result.inserted_id
    }
  )
  
  created["_id"] = str(created["_id"])
  return created

@router.get("/", response_model=List[ProfessorOut])
async def listar_professores(skip = 0, limit: int = 10):
  professores = await professores_collection.find().skip(skip).limit(limit).to_list(length=limit)
  
  for professor in professores:
    professor["_id"] = str(professor["_id"])
    
  return professor