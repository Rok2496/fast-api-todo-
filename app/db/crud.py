from sqlalchemy.orm import Session
from . import models
from ..schemas import schemas
from ..core import auth
from typing import Optional, List
import datetime

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user or not auth.verify_password(password, user.hashed_password):
        return None
    return user

def enable_2fa(db: Session, user: models.User, secret: str):
    user.two_factor_enabled = True
    user.two_factor_secret = secret
    db.commit()
    db.refresh(user)
    return user

def verify_2fa(db: Session, user: models.User, otp: str) -> bool:
    if not user.two_factor_secret:
        return False
    return auth.verify_2fa_token(user.two_factor_secret, otp)

def set_one_time_code(db: Session, user: models.User, code: str, expiry_minutes: int = 10) -> models.User:
    user.one_time_code = code
    user.one_time_code_expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiry_minutes)
    db.commit()
    db.refresh(user)
    return user

def verify_one_time_code(db: Session, email: str, code: str) -> Optional[models.User]:
    user = get_user_by_email(db, email)
    if not user or not user.one_time_code or user.one_time_code != code:
        return None
    
    # Check if code is expired
    if user.one_time_code_expiry < datetime.datetime.utcnow():
        return None
    
    # Clear the one-time code after use
    user.one_time_code = None
    user.one_time_code_expiry = None
    db.commit()
    db.refresh(user)
    
    return user

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int) -> models.Todo:
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_todos(db: Session, user_id: int) -> List[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.owner_id == user_id).all()

def get_todo(db: Session, todo_id: int, user_id: int) -> Optional[models.Todo]:
    return db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user_id).first()

def update_todo(db: Session, todo_id: int, user_id: int, todo_update: schemas.TodoUpdate) -> Optional[models.Todo]:
    todo = get_todo(db, todo_id, user_id)
    if not todo:
        return None
    for key, value in todo_update.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    todo.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int) -> bool:
    todo = get_todo(db, todo_id, user_id)
    if not todo:
        return False
    db.delete(todo)
    db.commit()
    return True 