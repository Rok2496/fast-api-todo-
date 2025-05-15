from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import timedelta
from ..db import crud
from ..db.database import SessionLocal
from ..db.models import User
from ..schemas import schemas
from ..api.deps import get_current_user, get_db
from ..services import google_calendar

router = APIRouter()

@router.post("", response_model=schemas.TodoOut)
def create_todo(todo: schemas.TodoCreate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    return crud.create_todo(db, todo, current_user.id)

@router.get("", response_model=List[schemas.TodoOut])
def read_todos(current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    return crud.get_todos(db, current_user.id)

@router.get("/{todo_id}", response_model=schemas.TodoOut)
def read_todo(todo_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    todo = crud.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    updated = crud.update_todo(db, todo_id, current_user.id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if not crud.delete_todo(db, todo_id, current_user.id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"msg": "Todo deleted"}

@router.post("/calendar/add")
def add_todo_to_calendar(todo_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    todo = crud.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if not current_user.google_refresh_token:
        raise HTTPException(status_code=400, detail="Google not connected")
    event_id = google_calendar.add_event_to_calendar(
        current_user.google_refresh_token,
        todo.title,
        todo.description or "",
        todo.due_date or todo.created_at,
        (todo.due_date or todo.created_at) + timedelta(hours=1)
    )
    return {"event_id": event_id} 