from fastapi import FastAPI
from app.api import user, todo

app = FastAPI()

app.include_router(user.router)
app.include_router(todo.router)
