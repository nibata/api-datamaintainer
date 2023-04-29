from typing import List
from sqlalchemy.orm import Session
from ...schemas.authentication import groups_schema
from ...models.authentication import groups as model_group
 
 
def get_group_by_id(db: Session, group_id: int):
    return db.query(model_group.Groups).filter(model_group.Groups.id == group_id).first()

 
def get_groups_by_id_list(db: Session, group_ids_list: List):
    return db.query(model_group.Groups).filter(model_group.Groups.id.in_(group_ids_list)).all()


def get_group_by_code(db: Session, code: str):
    return db.query(model_group.Groups).filter(model_group.Groups.code == code).first()


def get_groups(db: Session):
    return db.query(model_group.Groups).all()


def create_group(db: Session, group: groups_schema.GroupCreate):
    db_group = model_group.Groups(code=group.code,
                                  description=group.description)
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group
