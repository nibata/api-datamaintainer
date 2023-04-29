from .. import get_db
from typing import List
from ...auth import auth_bearer
from sqlalchemy.orm import Session
from ...schemas import groups_schema
from ...controller.authentication import groups_controller
from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.post("/groups", response_model=groups_schema.Group, dependencies=[Depends(auth_bearer.JWTBearer(required_permision=["ADMINISTRATOR"]))])
async def create_group(group: groups_schema.GroupCreate, db: Session = Depends(get_db)):
    db_user = groups_controller.get_group_by_code(db, code=group.code)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return groups_controller.create_group(db=db, group=group)
