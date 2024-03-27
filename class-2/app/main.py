from fastapi import  FastAPI
from typing import Union, Optional
from app import settings
from sqlmodel import Field,Session,SQLModel,create_engine,select

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str = Field(index=True)


Connection_string=str(settings.DATABASE_URL).replace("postgresql","postgresql+psycopg")

#start Engine
engine = create_engine(Connection_string,connect_args= {"sslmode":"require"}, pool_recycle=300)

#create db schema

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


app= FastAPI()

@app.get("/health/")
def health():
    create_db_and_tables()
    return {"status": "ok"}

@app.get("/")
def read_root():
    return{ "Hello": "World"}

@app.post("/todos/")
def create_todo(todo:Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.get("/todos/")
def read_todos():
    with Session(engine) as session:
        todos=session.exec(select(Todo)).all()
        return todos