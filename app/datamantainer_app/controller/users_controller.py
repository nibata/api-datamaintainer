from sqlalchemy import select
from sqlalchemy.orm import Session
from ..schemas import users_schemas
from ..models import users as model_users
from .groups_controller import get_groups_by_id_list
 
 
def get_user(db: Session, user_id: int):
    return db.query(model_users.Users).filter(model_users.Users.id == user_id).first()
 
 
def get_user_by_email(db: Session, email: str):
    return db.query(model_users.Users).filter(model_users.Users.email == email).first()
 
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_users.Users).offset(skip).limit(limit).all()
 
 
def create_user(db: Session, user: users_schemas.UserCreate):
    hashed_password = model_users.Users.set_password(user.password)
    db_user = model_users.Users(fullname=user.fullname,
                                email=user.email, 
                                hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_groups_from_user(db: Session, user_id: int):
    statement = select(model_users.users_groups).filter_by(user_id=user_id)
    groups = db.execute(statement).all()
    groups_list = [group["group_id"] for group in groups]
    
    rtn = get_groups_by_id_list(db, groups_list)

    return rtn



def check_user_password(db: Session, user: users_schemas.UserLogin):
    hashed_password = model_users.Users.set_password(user.password)
    db_user = get_user_by_email(db, user.email)
    
    if db_user is not None:
        rtn = db_user.hashed_password == hashed_password
        return rtn
    
    else:
        return False
