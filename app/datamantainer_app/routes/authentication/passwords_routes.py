from .. import get_db
from typing import List
from ...auth import auth_bearer
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ...schemas.authentication import password_schema
from ...controller.authentication import passwords_controller, users_controller


router = APIRouter()


@router.post("/password/create_password",
             response_model=password_schema.PasswordsBase,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["INSERT"]))])
async def create_password(form_user_pwd: password_schema.CreatePassword, db: Session = Depends(get_db)):
    db_user = users_controller.get_user_by_email(db, email=form_user_pwd.email)
    if  not db_user:
        raise HTTPException(status_code=400, detail="Email does not exists")
    
    # set password
    db_password = passwords_controller.create_password(db, db_user.id,
                                                       form_user_pwd.password,
                                                       form_user_pwd.expiration_date)

    return db_password


@router.post("/password/update_password",
             response_model=password_schema.PasswordsBase,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["INSERT"]))])
async def update_password(form_user_pwd: password_schema.UpdatePassword, db: Session = Depends(get_db)):
    db_user = users_controller.get_user_by_email(db, email=form_user_pwd.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email does not exists")
    
    # set password
    db_password = passwords_controller.update_password(db,
                                                       db_user.id,
                                                       form_user_pwd.current_password,
                                                       form_user_pwd.new_password,
                                                       form_user_pwd.expiration_date)

    return db_password
