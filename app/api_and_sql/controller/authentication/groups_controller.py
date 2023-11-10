from ...models.authentication import groups as model_group
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from typing import List


class GroupsController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_groups_by_id_list(self, group_ids_list: List):
        rtn = await self.session.execute(select(model_group.Group).where(model_group.Group.id.in_(group_ids_list)))
        return rtn.scalars().all()

    async def get_group_by_id(self, group_id: int):
        rtn = await self.session.execute(select(model_group.Group).where(model_group.Group.id == group_id))
        return rtn.scalars().first()

    async def get_group_by_code(self, code: str):
        rtn = await self.session.execute(select(model_group.Group).where(model_group.Group.code == code))
        return rtn.scalars().first()

    async def get_groups(self):
        rtn = await self.session.execute(select(model_group.Group))
        return rtn.scalars().all()

    async def create_group(self, group: model_group.GroupCreate):
        db_group = model_group.Group(code=group.code,
                                     description=group.description)

        self.session.add(db_group)
        await self.session.flush()

        return db_group
