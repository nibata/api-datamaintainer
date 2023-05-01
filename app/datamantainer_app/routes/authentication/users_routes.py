from .. import get_db
from typing import List
from ...auth import auth_bearer
from ...auth import auth_handler
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ...controller.authentication import users_controller
from ...controller.authentication import passwords_controller
from ...schemas.authentication import users_schemas, users_groups_schema


router = APIRouter()


@router.post("/user/login")
async def user_login(user: users_schemas.UserLogin, db:Session = Depends(get_db)):
    
    if users_controller.check_user_password(db=db, user=user):
        db_user = users_controller.get_user_by_email(db, email=user.email)
        roles = users_controller.get_groups_from_user(db=db, user_id=db_user.id)

        return auth_handler.signJWT(user_id=user.email, roles=roles)
    return {
        "error": "Wrong login details!"
    }


@router.post("/users", response_model=users_schemas.User, dependencies=[Depends(auth_bearer.JWTBearer(required_permision=["INSERT"]))])
async def create_user(user: users_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = users_controller.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # create user
    user_db = users_controller.create_user(db=db, user=user)
    
    # set password
    passwords_controller.create_password(db, user_db.id, user.password)

    return user_db

 
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


@router.post("/users/assign_role_to_user", dependencies=[Depends(auth_bearer.JWTBearer(required_permision=["ADMINISTRATOR"]))])
async def assign_role_to_user(user_group: users_groups_schema.UserAssignGroup, db: Session = Depends(get_db)):
    user_roles = [group.id for group in users_controller.get_groups_from_user(db=db, user_id=user_group.user_id)]
    user = users_controller.get_user(db=db, user_id=user_group.user_id)
    
    if user_group.group_id in user_roles:
        raise HTTPException(status_code=400, detail="The user is already assigned to this role")
    
    elif user is None:
        raise HTTPException(status_code=400, detail="The user doesn't exists")
    
    return users_controller.assign_role_to_user(db=db, user_id=user_group.user_id, group_id=user_group.group_id)
    