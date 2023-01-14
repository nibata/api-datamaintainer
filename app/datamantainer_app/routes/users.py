from fastapi import APIRouter, Depends, HTTPException
from ..schemas import users as schema_users
from ..controller import users as controller_user

from sqlalchemy.orm import Session

from . import get_db

from typing import List


router = APIRouter()

@router.post("/users/", response_model=schema_users.User)
def create_user(user: schema_users.UserCreate, db: Session = Depends(get_db)):
    db_user = controller_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return controller_user.create_user(db=db, user=user)
 
 
@router.get("/users/", response_model=List[schema_users.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = controller_user.get_users(db, skip=skip, limit=limit)
    return users
 
 
@router.get("/users/{user_id}", response_model=schema_users.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = controller_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user