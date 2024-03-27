from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from contextlib import asynccontextmanager
from typing import Annotated

from app import settings

class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str

connection_string: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(connection_string)

def create_tables():
    print("Creating tables")
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    create_tables()
    yield
    print("Application shutdown")

app: FastAPI = FastAPI(lifespan=lifespan)

async def get_session():
    with Session(engine) as session:
        yield session

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get("/db")
def db():
    return {"ENV_SECRET": settings.DATABASE_URL, "CONNECTION_STRING": connection_string}

# POST ROUTE to create a new todo
@app.post("/todos")
def create_todo(todo: Todo, session: Annotated[Session, Depends(get_session)]):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
    
# GET ROUTE to list all todos
@app.get("/todos")
def list_todos(session: Annotated[Session, Depends(get_session)]):
    todos = session.exec(select(Todo)).all()
    return todos