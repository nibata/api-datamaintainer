from sqlalchemy.orm import Session
from sqlalchemy import select, insert
#from .passwords_controller import check_password
from .passwords_controller import PasswordsController
from ...schemas.authentication import users_schemas
#from .groups_controller import get_groups_by_id_list
from .groups_controller import GroupsController
from ...models.authentication import users as model_users


class UsersController:
    def __init__(self, session: Session):
        self.session = session

    async def get_user(self, user_id: int):
        rtn = await self.session.execute(select(model_users.Users).where(model_users.Users.id == user_id))
        return rtn.scalars().first()

    async def get_users(self, skip: int = 0, limit: int = 100):
        rtn = await self.session.execute(select(model_users.Users).offset(skip).limit(limit))
        return rtn.scalars().all()

    async def get_user_by_email(self, email: str):
        rtn = await self.session.execute(select(model_users.Users).where(model_users.Users.email == email))
        return rtn.scalars().first()

    async def check_user_password(self, user: users_schemas.UserLogin):
        password = user.password
        db_user = await self.get_user_by_email(user.email)
        password_controller = PasswordsController(self.session)
        return await password_controller.check_password(db_user.id, password)

    async def get_groups_from_user(self, user_id: int):
        statement = select(model_users.users_groups).where(model_users.users_groups.c.user_id == user_id)

        groups = await self.session.execute(statement)
        groups = groups.all()

        groups_list = [group["group_id"] for group in groups]

        group_controller = GroupsController(self.session)
        rtn = await group_controller.get_groups_by_id_list(groups_list)

        return rtn

    async def create_user(self, user: users_schemas.UserCreate):
        db_user = model_users.Users(fullname=user.fullname,
                                    email=user.email)

        self.session.add(db_user)
        await self.session.flush()

        return db_user


def assign_role_to_user(db: Session, user_id: int, group_id: int):
    statement = insert(model_users.users_groups).values(user_id=user_id, group_id=group_id)
    db.execute(statement)
    db.commit()

    return {'user_id': user_id,
            'group_id': group_id}



