from fastapi import FastAPI

from app import settings

todo_server: FastAPI = FastAPI()

@todo_server.get("/")
def hello():
    return {"Hello": "World"}

@todo_server.get("/db")
def db_var():
    return {"DB": settings.DATABASE_URL}

