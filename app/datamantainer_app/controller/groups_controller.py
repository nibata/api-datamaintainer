from typing import List
from sqlalchemy.orm import Session
from ..schemas import groups_schema
from ..models import groups as model_group
 
 
def get_group_by_id(db: Session, group_id: int):
    return db.query(model_group.Groups).filter(model_group.Groups.id == group_id).first()

 
def get_groups_by_id_list(db: Session, group_ids_list: List):
    return db.query(model_group.Groups).filter(model_group.Groups.id.in_(group_ids_list)).all()


def get_groups(db: Session):
    return db.query(model_group.Groups).all()


def create_user(db: Session, group: groups_schema.GroupCreate):
    db_group = model_group.Groups(code=group.code,
                                  description=group.description)
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group
