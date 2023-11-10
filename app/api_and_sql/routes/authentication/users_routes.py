from ...controller.authentication.passwords_controller import PasswordsController
from ...controller.authentication.groups_controller import GroupsController
from ...controller.authentication.users_controller import UsersController
from ...models.authentication.users import UserLogin, UserCreate, User
from ...models.authentication.users_groups import UserGroupLink
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession
from ...configs.database import get_session
from typing import List, Annotated
from ...auth import auth_handler
from ...auth import auth_bearer


router = APIRouter()


@router.post("/user/login", tags=["Authentication"])
async def user_login(user: UserLogin, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        password_match = await user_controller.check_user_password(user=user)
        user_obj = await user_controller.get_user_by_email(email=user.email)

        if user_obj is not None and password_match:
            is_user_active = user_obj.is_active

            if password_match and is_user_active:
                db_user = await user_controller.get_user_by_email(email=user.email)
                roles = await user_controller.get_groups_from_user(user_id=db_user.id)

                return auth_handler.sign_jwt(user_id=user.email, roles=roles)

            if not is_user_active:
                return {
                    "error": "User is not longer active"
                }

        return {
            "error": "Wrong login details"
        }


@router.post("/users",
             response_model=User,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["INSERT"]))],
             tags=["Authentication"])
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)
        group_controller = GroupsController(session)

        db_user = await user_controller.get_user_by_email(email=user.email)
        group_db = await group_controller.get_group_by_code("DEFAULT")

        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # create user
        user_db = await user_controller.create_user(user=user)

        # set password
        await password_controller.create_password(user_id=user_db.id,
                                                  password=user.password,
                                                  expiration_date=user.expiration_date)

        await user_controller.assign_role_to_user(user_id=user_db.id,
                                                  group_id=group_db.id)

        # obtengo usuario de base de datos (el objeto user_db no esta linkeado a la session)
        rtn = await user_controller.get_user(user_id=user_db.id)

        session.expunge_all()

        return rtn


@router.get("/users", response_model=List[User], tags=["Authentication"])
async def read_users(skip: int = 0, limit: int = 100, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        db_users = await user_controller.get_users(skip=skip, limit=limit)

        session.expunge_all()

        return db_users


@router.get("/users/q",
            response_model=User,
            tags=["Authentication"])
async def read_user(user_id: Annotated[int | None, Query(alias="user-id")] = None,
                    user_email: Annotated[str | None, Query(alias="user-email")] = None,
                    session: AsyncSession = Depends(get_session)):
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
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))],
             tags=["Authentication"])
async def assign_role_to_user(user_group: UserGroupLink, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        group_controller = GroupsController(session)

        user_roles = [group.id for group in await user_controller.get_groups_from_user(user_id=user_group.user_id)]
        user = await user_controller.get_user(user_id=user_group.user_id)
        group = await group_controller.get_group_by_id(group_id=user_group.group_id)

        if user_group.group_id in user_roles:
            raise HTTPException(status_code=400, detail="The user is already assigned to this role")

        elif user is None:
            raise HTTPException(status_code=400, detail="The user doesn't exists")

        elif group is None:
            raise HTTPException(status_code=400, detail="The role doesn't exists")

        return await user_controller.assign_role_to_user(user_id=user_group.user_id, group_id=user_group.group_id)
