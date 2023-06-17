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

    async def get_group_by_id(self, group_id: int):
        rtn = await self.session.execute(select(model_group.Groups).where(model_group.Groups.id == group_id))
        return rtn.scalars().first()

    async def get_group_by_code(self, code: str):
        rtn = await self.session.execute(select(model_group.Groups).where(model_group.Groups.code == code))
        return rtn.scalars().first()

    async def get_groups(self):
        rtn = await self.session.execute(select(model_group.Groups))
        return rtn.scalars().all()

    async def create_group(self, group: groups_schema.GroupCreate):
        db_group = model_group.Groups(code=group.code,
                                      description=group.description)

        self.session.add(db_group)
        await self.session.flush()

        return db_group
