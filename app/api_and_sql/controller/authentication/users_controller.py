from ...models.authentication import users_groups as model_user_group_link
from ...models.authentication import users as model_users
from sqlmodel.ext.asyncio.session import AsyncSession
from .passwords_controller import PasswordsController
from .groups_controller import GroupsController
from sqlmodel import select, insert


class UsersController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user(self, user_id: int):
        rtn = await self.session.execute(select(model_users.User).where(model_users.User.id == user_id))
        return rtn.scalars().first()

    async def get_users(self, skip: int = 0, limit: int = 100):
        rtn = await self.session.execute(select(model_users.User).offset(skip).limit(limit))
        return rtn.scalars().all()

    async def get_user_by_email(self, email: str):
        rtn = await self.session.execute(select(model_users.User).where(model_users.User.email == email))
        return rtn.scalars().first()

    async def check_user_password(self, user: model_users.UserLogin):
        password = user.password
        db_user = await self.get_user_by_email(user.email)

        if db_user is None:
            return False

        password_controller = PasswordsController(self.session)

        return await password_controller.check_password(db_user.id, password)

    async def get_groups_from_user(self, user_id: int):
        statement = (select(model_user_group_link.UserGroupLink).
                     where(model_user_group_link.UserGroupLink.user_id == user_id))

        groups = await self.session.execute(statement)
        groups = groups.all()

        groups_list = [group[0].group_id for group in groups]

        group_controller = GroupsController(self.session)
        rtn = await group_controller.get_groups_by_id_list(groups_list)

        return rtn

    async def create_user(self, user: model_users.UserCreate):
        db_user = model_users.User(full_name=user.full_name,
                                   email=user.email)

        self.session.add(db_user)
        await self.session.flush()

        return db_user

    async def assign_role_to_user(self, user_id: int, group_id: int):
        statement = insert(model_user_group_link.UserGroupLink).values(user_id=user_id, group_id=group_id)
        await self.session.execute(statement)
        await self.session.flush()

        return {'UserId': user_id,
                'GroupId': group_id}

    async def set_is_active_user(self, user_id: int, is_active: bool):
        """
        Set the user state. In oder word change de property is_active for the model users
        :param user_id: the id of the user whose state is to be set.
        :param is_active: the final value of the state
        :return: model user
        """

        statement = select(model_users.User).where(model_users.User.id == user_id)
        result = await self.session.execute(statement)
        user = result.scalar_one()

        user.is_active = is_active

        return user
