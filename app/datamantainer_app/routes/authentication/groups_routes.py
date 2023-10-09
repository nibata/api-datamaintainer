from ...controller.authentication.groups_controller import GroupsController
from ...models.authentication.groups import GroupRead, GroupCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ...configs.database import get_session
from ...auth import auth_bearer


router = APIRouter()


@router.post("/groups",
             response_model=GroupRead,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))],
             tags=["Authentication"])
async def create_group(group: GroupCreate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        group_controller = GroupsController(session)
        db_group = await group_controller.get_group_by_code(code=group.code)

        if db_group:
            raise HTTPException(status_code=400, detail="Group already Exists")

        group_db = await group_controller.create_group(group=group)

        rtn = await group_controller.get_group_by_id(group_id=group_db.id)

        session.expunge_all()

        return rtn
