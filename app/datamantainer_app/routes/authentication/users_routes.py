from ...controller.authentication.passwords_controller import PasswordsController
from ...controller.authentication.groups_controller import GroupsController
from ...controller.authentication.users_controller import UsersController
from ...models.authentication.users_groups import UserGroupLink
from ...models.authentication.users import UserLogin, UserCreate, User
from fastapi import APIRouter, Depends, HTTPException
#from ...configs.database import SessionLocal
from ...configs.database import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ...auth import auth_handler
from ...auth import auth_bearer
from typing import List


router = APIRouter()


@router.post("/user/login")
async def user_login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        password_match = await user_controller.check_user_password(user=user)
        user_obj = await user_controller.get_user_by_email(email=user.Email)

        if user_obj is not None and password_match:
            is_user_active = user_obj.IsActive

            if password_match and is_user_active:
                db_user = await user_controller.get_user_by_email(email=user.Email)
                roles = await user_controller.get_groups_from_user(user_id=db_user.Id)

                return auth_handler.sign_jwt(user_id=user.Email, roles=roles)

            if not is_user_active:
                return {
                    "error": "User is not longer active"
                }

        return {
            "error": "Wrong login details"
        }


@router.post("/users",
             response_model=User,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["INSERT"]))])
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)
        group_controller = GroupsController(session)

        db_user = await user_controller.get_user_by_email(email=user.Email)
        group_db = await group_controller.get_group_by_code("DEFAULT")

        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # create user
        user_db = await user_controller.create_user(user=user)

        # set password
        await password_controller.create_password(user_id=user_db.Id,
                                                  password=user.Password,
                                                  expiration_date=user.ExpirationDate)

        await user_controller.assign_role_to_user(user_id=user_db.Id,
                                                  group_id=group_db.Id)

        # obtengo usuario de base de datos (el objeto user_db no esta linkeado a la session)
        rtn = await user_controller.get_user(user_id=user_db.Id)

        session.expunge_all()

        return rtn


@router.get("/users", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        db_users = await user_controller.get_users(skip=skip, limit=limit)

        session.expunge_all()

        return db_users


@router.get("/users/q",
            response_model=User)
async def read_user(user_id: int | None = None, user_email: str | None = None, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        if user_id is not None:
            user_controller = UsersController(session)
            db_user = await user_controller.get_user(user_id=user_id)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")

            session.expunge_all()

            return db_user

        elif user_email is not None:
            user_controller = UsersController(session)
            db_user = await user_controller.get_user_by_email(email=user_email)

            if db_user is None:
                raise HTTPException(status_code=404, detail="User not found")

            session.expunge_all()

            return db_user

        else:
            raise HTTPException(status_code=404, detail="Not given user")


@router.post("/users/assign_role_to_user",
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def assign_role_to_user(user_group: UserGroupLink, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        group_controller = GroupsController(session)

        user_roles = [group.Id for group in await user_controller.get_groups_from_user(user_id=user_group.UserId)]
        user = await user_controller.get_user(user_id=user_group.UserId)
        group = await group_controller.get_group_by_id(group_id=user_group.GroupId)

        if user_group.GroupId in user_roles:
            raise HTTPException(status_code=400, detail="The user is already assigned to this role")

        elif user is None:
            raise HTTPException(status_code=400, detail="The user doesn't exists")

        elif group is None:
            raise HTTPException(status_code=400, detail="The role doesn't exists")

        return await user_controller.assign_role_to_user(user_id=user_group.UserId, group_id=user_group.GroupId)
