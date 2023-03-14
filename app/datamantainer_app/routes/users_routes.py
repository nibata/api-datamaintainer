from . import get_db
from typing import List
from ..auth import auth_bearer
from ..auth import auth_handler
from sqlalchemy.orm import Session
from ..schemas import users_schemas
from ..controller import users_controller
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.post("/user/login")
async def user_login(user: users_schemas.UserLogin, db:Session = Depends(get_db)):
    if users_controller.check_user_password(db=db, user=user):
        return auth_handler.signJWT(user_id=user.email, roles=["SELECT"])
    return {
        "error": "Wrong login details!"
    }


@router.post("/users", response_model=users_schemas.User, dependencies=[Depends(auth_bearer.JWTBearer(required_permision=["SELECT"]))])
async def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users_controller.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return users_controller.create_user(db=db, user=user)
 
 
@router.get("/users", response_model=List[users_schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = users_controller.get_users(db, skip=skip, limit=limit)
    return users
 
 
@router.get("/users/q", response_model=users_schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = users_controller.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
