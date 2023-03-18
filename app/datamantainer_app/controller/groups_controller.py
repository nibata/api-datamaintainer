from sqlalchemy.orm import Session
from ..schemas import groups_schema
from ..models import groups as model_group
 
 
def get_group(db: Session, group_id: int):
    return db.query(model_group.Groups).filter(model_group.Groups.id == group_id).first()
 

def create_user(db: Session, group: groups_schema.GroupCreate):
    db_group = model_group.Groups(code=group.code,
                                  description=group.description)
    
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group
