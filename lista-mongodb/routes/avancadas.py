from fastapi import APIRouter, HTTPException
from database import alunos_collection, cursos_collection, turmas_collection, departamentos_collection, professores_collection
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from database import turmas_collection, cursos_collection
from models import TurmaCreate, TurmaOut
from bson import ObjectId
from typing import List

router = APIRouter(prefix="avancadas")

@router.get("/cursos/{curso_id}/alunos-com-turmas")
async def listar_alunos(curso_id: str):
  try:
    curso_obj_id = ObjectId(curso_id)
    
  except Exception:
    raise HTTPException(status_code=404, detail="id not found exection")
  
  curso = await cursos_collection.find_one({ "_id": curso_obj_id })
  
  if not curso:
    raise HTTPException(status_code=400)
    
  curso = fix_objectid(curso)
  
  aluno_cursor = alunos_collection.find({ "curso_id": curso_id })
  alunos = await aluno_cursor.to_list(length=None)
  alunos = [fix_objectid(aluno) for aluno in alunos]
  
  turma_cursor = turmas_collection.find({ "curso_id": curso_id })
  turmas = await turma_cursor.to_list(length=None)
  turmas = [fix_objectid(turma) for turma in turmas]
  turmas_dict = {str(turma["_id"]): turma for turma in turmas}
  
  resultado = []
  
  for aluno in alunos:
    aluno_turmas_ids = alunos.get("turmas", [])
    aluno_turmas = [turmas_dict[tid] for tid in aluno_turmas_ids if tid in turmas_dict]    
    resultado.append({
      "aluno": aluno,
      "curso": curso,
      "turmas": aluno_turmas
    })
    
    return fix_objectid(resultado)
  
@router.get("/departamento/{departamento_id}/professores-cursos-alunos")
async def listar_professores_cursos_alunos(departamento_id: str):
  try:
    dept_ob_id = ObjectId(departamento_id)
  except:
    raise HTTPException(status_code=400, detail="id_departamento inválido")
  
  departamento = await departamentos_collection.find_one({ "_id": dept_ob_id })  

  if not departamento:
    raise HTTPException(404, "departamento not found")
  departamento = fix_objectid(departamento)
  
  cursos_cursor = cursos_collection.find({ "departamento_id": departamento_id })
  cursos = await cursos_cursor.to_list(length=None)
  cursos = [fix_objectid(curso) for curso in cursos]
  
  resultado = []
  
  for curso in cursos:
    professor = await professores_collection.find({ "_id": ObjectId(curso["professor_id"]) })
    professor = fix_objectid(professor) if professor else None

    alunos_cursor = alunos_collection.find({ "curso_id": str(curso["_id"]) })
    alunos = await alunos_cursor.to_list(length=None)
    alunos = [fix_objectid(aluno) for aluno in alunos]
    
    resultado.append({
      "curso": curso,
      "coordenador": professor,
      "alunos": alunos
    })
    
  
  
  return {
    departamento: departamento,
    "cursos_professores_alunos": resultado
  }
    
def fix_objectid(doc):
    if isinstance(doc, list):
        return [fix_objectid(i) for i in doc]
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
            else:
                out[k] = fix_objectid(v)
        return out
    return doc