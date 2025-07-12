
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Aluno(Model):
  __keyspace__ = "escola2"
  matricula = columns.Text(primary_key=True)
  nome = columns.Text(required = True)
  curso = columns.Text(required = True)
  ano = columns.Integer(required = True)
  
class Disciplina(Model):
  __keyspace__ = "escola2"
  codigo = columns.Text(primary_key=True)
  codigo = columns.Text(primary_key=True)
  codigo = columns.Text(primary_key=True)
  
class AlunoDisciplina(Model):
  __keyspace__ = "escola2"
  matricula = columns.Text(primary_key = True)
  codigo_disciplina = columns.Text(primary_key = True, partion_key=True)