from ...auth import auth_bearer
from ...configs.database import SessionLocal
from ...schemas.authentication import groups_schema
from fastapi import APIRouter, Depends, HTTPException
from ...controller.authentication.groups_controller import GroupsController


router = APIRouter()


@router.post("/groups",
             response_model=groups_schema.Group,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def create_group(group: groups_schema.GroupCreate):
    async with SessionLocal() as session:
        async with session.begin():
            group_controller = GroupsController(session)
            db_group = await group_controller.get_group_by_code(code=group.code)

            if db_group:
                raise HTTPException(status_code=400, detail="Group already Exists")

            group_db = await group_controller.create_group(group=group)

            rtn = await group_controller.get_group_by_id(group_id=group_db.id)

            session.expunge_all()

            return rtn
