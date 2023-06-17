from .. import get_db
from typing import List
from ...auth import auth_bearer
from ...auth import auth_handler
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from ...controller.authentication import users_controller
from ...schemas.authentication import users_schemas, users_groups_schema

from ...controller.authentication.users_controller import UsersController
from ...controller.authentication.passwords_controller import PasswordsController

from ...configs.database import SessionLocal


router = APIRouter()


@router.post("/user/login")
async def user_login(user: users_schemas.UserLogin):
    async with SessionLocal() as session:
        async with session.begin():
            user_controller = UsersController(session)
            password_match = await user_controller.check_user_password(user=user)

            if password_match:
                db_user = await user_controller.get_user_by_email(email=user.email)
                roles = await user_controller.get_groups_from_user(user_id=db_user.id)

                return auth_handler.sign_jwt(user_id=user.email, roles=roles)

            return {
                "error": "Wrong login details!"
            }


@router.post("/users",
             response_model=users_schemas.User,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["INSERT"]))])
async def create_user(user: users_schemas.UserCreate):
    async with SessionLocal() as session:
        async with session.begin():
            user_controller = UsersController(session)
            password_controller = PasswordsController(session)
            db_user = await user_controller.get_user_by_email(email=user.email)

            if db_user:
                raise HTTPException(status_code=400, detail="Email already registered")

            # create user
            user_db = await user_controller.create_user(user=user)

            # set password
            await password_controller.create_password(user_id=user_db.id,
                                                      password=user.password,
                                                      expiration_date=user.expiration_date)

            # obtengo usuario de base de datos (el objeto user_db no esta linkeado a la session)
            rtn = await user_controller.get_user(user_id=user_db.id)

            session.expunge_all()

            return rtn


@router.get("/users",
            response_model=List[users_schemas.User])
async def read_users(skip: int = 0, limit: int = 100):
    async with SessionLocal() as session:
        async with session.begin():
            user_controller = UsersController(session)
            db_users = await user_controller.get_users(skip=skip, limit=limit)
            session.expunge_all()

            return db_users


@router.get("/users/q",
            response_model=users_schemas.User)
async def read_user(user_id: int):
    async with SessionLocal() as session:
        async with session.begin():
            user_controller = UsersController(session)
            db_user = await user_controller.get_user(user_id=user_id)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")

            session.expunge_all()

            return db_user


@router.post("/users/assign_role_to_user",
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def assign_role_to_user(user_group: users_groups_schema.UserAssignGroup, db: Session = Depends(get_db)):
    user_roles = [group.id for group in users_controller.get_groups_from_user(db=db, user_id=user_group.user_id)]
    user = users_controller.get_user(db=db, user_id=user_group.user_id)
    
    if user_group.group_id in user_roles:
        raise HTTPException(status_code=400, detail="The user is already assigned to this role")
    
    elif user is None:
        raise HTTPException(status_code=400, detail="The user doesn't exists")
    
    return users_controller.assign_role_to_user(db=db, user_id=user_group.user_id, group_id=user_group.group_id)
    