from sqlmodel.ext.asyncio.session import AsyncSession
from ..models.testmodel import TestTable
from sqlmodel import select


class TestController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_test(self):
        result = await self.session.execute(select(TestTable).where(TestTable.id > 0))
        rtn = result.scalars().all()
        return rtn
