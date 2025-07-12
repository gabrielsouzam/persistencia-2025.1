from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.query import DoesNotExist
from cassandra.cluster import Cluster
import time

from models import Aluno, Disciplina, AlunoDisciplina

def criar_keyspace_escola():
  cluster = Cluster(['127.0.0.1'])
  session = cluster.connect()
  session.execute(
    """
    CREATE KEYSPACE IF NOT EXISTS escola2
    WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 } 
    """
  )  
  session.shutdown()
  cluster.shutdown()

class AlunoIn(BaseModel):
  matricula: str
  nome: str
  curso: str
  ano: int
  
class AlunoOut(AlunoIn):
  pass

class DisciplinaIn(BaseModel):
  codigo: str
  nome: str
  professor: str

class DisciplinaOut(DisciplinaIn):
  pass

class AlunoDisciplinaIn(BaseModel):
  matricula: str
  codigo_disciplina: str

class AlunoDisciplinaOut(AlunoDisciplinaIn):
  pass


app = FastAPI(title="CRUD Cassandra + FASTAPI + ORM")

@app.on_event("startup")
def startup():
  criar_keyspace_escola()
  time.sleep()
  connection.setup('127.0.0.1', "escola2", protocol_version=3)
  sync_table(Aluno)
  sync_table(Disciplina)
  sync_table(AlunoDisciplina)
  
@app.post("/alunos/", response_model=AlunoOut)
def criar_aluno(aluno: AlunoIn):
  try:
    obj = Aluno.create(**aluno.model_dump())
    return AlunoOut(**dict(obj))
  except Exception as e:
    raise HTTPException(status_code=400, detail=str(e))
    

@app.get("alunos/{matricula}", response_model=AlunoOut)
def obter_aluno_por_matricula(matricula: str):
  try:
    aluno = Aluno.get(matricula = matricula)
    return AlunoOut(**dict(aluno))
  except DoesNotExist:
    raise HTTPException(status_code=404, detail="aluno nao encontrado")
  
@app.get("/alunos/get", response_model=list[AlunoOut])
def listar_alunos():
  return [AlunoOut(**dict(a)) for a in Aluno.all()]


@app.get("/alunos/get", response_model=list[AlunoOut])
def listar_alunos_paginados(
  page: int = Query(1, gt = 0),
  page_size: int = Query(10, gt = 0, len=100)
):
  offset = (page - 1) * page_size
  alunos = list(Aluno.all())
  paginados = alunos[offset:offset+page_size]
  
  return [AlunoOut(**dict(a)) for a in paginados]
  
@app.put("/alunos/{matricula}", response_model=AlunoOut)
def atualizar_aluno(matricula: str, dados: AlunoIn):
  try:
    aluno = Aluno.get(matricula=matricula)
    aluno.update(**dados.model_dump())
    aluno_atualizado = Aluno.get(matricula=matricula)
    
    return AlunoOut(**dict(aluno_atualizado))
  except DoesNotExist:
    raise HTTPException(status_code=404,detail="Aluno não encontrado")
  

@app.delete("/alunos/{matricula}", response_model=str)
def deletar_aluno(matricula: str):
  try:
    aluno = Aluno.get(matricula=matricula)
    aluno.delete()
    
    return {
      "detail": "Aluno removido com sucesso"
    }
  except DoesNotExist:
    raise HTTPException(status_code=404, detail="Aluno não encontrado")
  
@app.post("/disciplinas/", response_model=DisciplinaOut)
def criar_disciplina(disciplina: DisciplinaIn):
    try:
        obj = Disciplina.create(**disciplina.dict())
        return DisciplinaOut(**dict(obj))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/disciplinas/{codigo}", response_model=DisciplinaOut)
def obter_disciplina(codigo: str):
    try:
        disciplina = Disciplina.get(codigo=codigo)
        return DisciplinaOut(**dict(disciplina))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")

@app.get("/disciplinas/", response_model=list[DisciplinaOut])
def listar_disciplinas():
    return [DisciplinaOut(**dict(d)) for d in Disciplina.all()]

@app.delete("/disciplinas/{codigo}")
def deletar_disciplina(codigo: str):
    try:
        disciplina = Disciplina.get(codigo=codigo)
        disciplina.delete()
        return {"detail": "Disciplina removida com sucesso"}
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Disciplina não encontrada")
      
@app.post("/alunos/{matricula}/disciplina/{codigo_disciplina}", response_model=AlunoDisciplinaOut)
def matricular_aluno_disciplina(
  matricula: str,
  codigo_disciplina: str
):
  try:
    Aluno.get(matricula=matricula)
    Disciplina.get(codigo=codigo_disciplina)
  except DoesNotExist:
    raise HTTPException(status_code=404, detail="Disciplina não encontrada")
  
  obj = AlunoDisciplina.create(matricula=matricula, codigo_disciplina=codigo_disciplina)
  
  return AlunoDisciplinaOut(**dict(obj))

@app.get("/alunos/{matricula}/disciplinas/", response_model=list[DisciplinaOut])
def listar_disciplina_do_aluno(matricula: str):
  associantions = AlunoDisciplina.filter(matricula=matricula)
  codigos = [a.codigo_disciplina for a in associantions]
  if not codigos:
    return []
  
  return [DisciplinaOut(**dict(d)) for d in Disciplina.object.filter()]