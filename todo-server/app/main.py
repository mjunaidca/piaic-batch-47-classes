from fastapi import FastAPI
from sqlmodel import SQLModel, Field, create_engine, Session
from contextlib import asynccontextmanager

from app import settings

# Step 1: Database Table SCHEMA
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str


# Connection to the database
conn_str: str = str(settings.DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

engine = create_engine(conn_str)

def create_db_tables():
    print("create_db_tables")
    SQLModel.metadata.create_all(engine)
    print("done")

@asynccontextmanager
async def lifespan(todo_server: FastAPI):
    print("Server Startup")
    create_db_tables()
    yield

# Table Data Save, Get

todo_server: FastAPI = FastAPI(lifespan=lifespan)


@todo_server.post("/todo")
def create_todo(try_content: Todo):
        session = Session(engine)
        session.add(try_content)
        session.commit()
        session.refresh(try_content)
        session.close()
        return try_content
