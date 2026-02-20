from fastapi import APIRouter, Depends
from app.models.todo import CreateTodo
from typing import Annotated
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.schema.todo_schema import TodoSchema

router =APIRouter(
    prefix="/todos",
    tags=["todos"]
)

@router.get("/")
def get_todos():
    return {"Message": "Get all todos"}

@router.post("/")
def create_todo(item:CreateTodo, db: Annotated[Session, Depends(get_db)]):
    todo = TodoSchema(**item.model_dump())
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return {"Message": "Create a new todo", "item": todo} # item.model_dump()