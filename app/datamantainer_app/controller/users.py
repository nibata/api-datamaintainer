from sqlalchemy.orm import Session

from ..models import users as model_users
 
from ..schemas import users as schema_users
 
 
def get_user(db: Session, user_id: int):
    return db.query(model_users.Users).filter(model_users.Users.id == user_id).first()
 
 
def get_user_by_email(db: Session, email: str):
    return db.query(model_users.Users).filter(model_users.Users.email == email).first()
 
 
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_users.Users).offset(skip).limit(limit).all()
 
 
def create_user(db: Session, user: schema_users.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = model_users.Users(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user