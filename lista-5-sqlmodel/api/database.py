from sqlmodel import SQLModel, create_engine

sqlite_file_name = "app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    from api.models.models import Equipe, Membro, Projeto, Tarefa, Membership
    SQLModel.metadata.create_all(engine)