from .. import get_db
from typing import List
from ...auth import auth_bearer
from sqlalchemy.orm import Session
from ...schemas.authentication import groups_schema
from fastapi import APIRouter, Depends, HTTPException
from ...controller.authentication import groups_controller


router = APIRouter()


@router.post("/groups",
             response_model=groups_schema.Group,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def create_group(group: groups_schema.GroupCreate, db: Session = Depends(get_db)):
    db_group = groups_controller.get_group_by_code(db, code=group.code)
    if db_group:
        raise HTTPException(status_code=400, detail="Group already Exists")
    return groups_controller.create_group(db=db, group=group)
