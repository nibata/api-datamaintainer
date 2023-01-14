from sqlalchemy.orm import Session
from ..schemas import users_schemas
from ..models import users as model_users
 
 
def get_user(db: Session, user_id: int):
    return db.query(model_users.Users).filter(model_users.Users.id == user_id).first()
 
 
def get_user_by_email(db: Session, email: str):
    return db.query(model_users.Users).filter(model_users.Users.email == email).first()
 
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_users.Users).offset(skip).limit(limit).all()
 
 
def create_user(db: Session, user: users_schemas.UserCreate):
    hashed_password = model_users.Users.set_password(user.password)
    db_user = model_users.Users(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
