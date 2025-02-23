from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from app.schemas.todo import TodoCreateUpdate
from app.models.todo import Todo
from app.models.user import User
from app.core.security import decode
from app.db.engine import get_db

router = APIRouter()


@router.get("/todos")
def get_todos(page: Annotated[int, Query(ge=1)] = 1, limit: Annotated[int, Query(ge=1, le=10)] = 10, token: str = Depends(decode), session: Session = Depends(get_db)):
    user_id = session.exec(select(User.id).where(
        User.email == token["email"])).one()
    total_items = session.exec(
        select(func.count()).where(Todo.user_id == user_id)).one()
    offest = (page - 1) * limit
    res = session.exec(
        select(Todo).where(Todo.user_id == user_id).offset(offest).limit(limit)).all()
    page_data = [todo.model_dump(exclude={"user_id"}) for todo in res]
    return {"data": page_data, "page": page, "limit": limit, "total": total_items}


@router.post("/todos")
def create_todos(todo_data: TodoCreateUpdate, token: str = Depends(decode), session: Session = Depends(get_db)):
    user_email = token["email"]
    user_id = session.exec(select(User.id).where(
        User.email == user_email)).one()
    title = todo_data.title
    description = todo_data.description
    new_data = Todo(title=title, description=description, user_id=user_id)
    session.add(new_data)
    session.commit()
    todo_id = new_data.id
    return {"id": todo_id, "title": title, "description": description}


@router.put("/todos/{id}")
def update_todos(id, todo_data: TodoCreateUpdate, token: str = Depends(decode), session: Session = Depends(get_db)):
    auth = check_auth(id, token, session)
    if auth:
        title = todo_data.title
        description = todo_data.description
        raw_data = session.exec(select(Todo).where(Todo.id == id)).one()
        raw_data.title = title
        raw_data.description = description
        session.add(raw_data)
        session.commit()
    return {"id": id, "title": title, "description": description}


@router.delete("/todos/{id}")
def delete_todos(id, token: str = Depends(decode), session: Session = Depends(get_db)):
    auth = check_auth(id, token, session)
    if auth:
        data = session.exec(select(Todo).where(Todo.id == id)).one()
        session.delete(data)
        session.commit()
    return status.HTTP_204_NO_CONTENT


def check_auth(id, token, session: Session = Depends(get_db)):
    current_user_email = token["email"]
    current_user_id = session.exec(select(User.id).where(
        User.email == current_user_email)).one()
    todo_user_id = session.exec(
        select(Todo.user_id).where(Todo.id == id)).one()
    if todo_user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return True
