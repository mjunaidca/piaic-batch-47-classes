from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from app import settings
from contextlib import asynccontextmanager

class ToDo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    content: str

connection_string = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(
    connection_string
)

def create_tables():
    print("DB_URL\n", connection_string)
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def LahoreClass(app: FastAPI):
    print("Creating tables..")
    create_tables()
    yield

app = FastAPI(lifespan=LahoreClass)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# 1. Create Todo
@app.post("/todo")
def create_todo(todo_content: ToDo):
    with Session(engine) as session:
        session.add(todo_content)
        session.commit()

    return todo_content

@app.get("/todo")
def get_todo():
    with Session(engine) as session:
        query = session.exec(ToDo).all()
        return query