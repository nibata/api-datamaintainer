from typing import List
from sqlalchemy import select
from sqlalchemy.orm import Session
from ...schemas.authentication import groups_schema
from ...models.authentication import groups as model_group
 

class GroupsController:
    def __init__(self, session: Session):
        self.session = session

    async def get_groups_by_id_list(self, group_ids_list: List):
        rtn = await self.session.execute(select(model_group.Groups).where(model_group.Groups.id.in_(group_ids_list)))
        return rtn.scalars().all()


def get_group_by_id(db: Session, group_id: int):
    return db.query(model_group.Groups).filter(model_group.Groups.id == group_id).first()


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
