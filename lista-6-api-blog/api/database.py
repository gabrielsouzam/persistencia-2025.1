from sqlmodel import SQLModel, Session, create_engine

sqlite_file_name = "blog.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    from api.models.models import User, Post, Category, Comment, Like, PostCategory
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session