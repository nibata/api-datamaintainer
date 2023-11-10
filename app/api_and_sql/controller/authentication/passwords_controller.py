from ...models.authentication import passwords as model_password
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from sqlmodel import select
from datetime import date


class PasswordsController:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_password(self, user_id: int) -> str:
        """Get the current active password.

        Parameters
        ----------
        user_id : int
            User's id that is wanted to get the current password

        Returns
        -------
        str
            Current active password
        """

        password = await self.session.execute(select(model_password.Password).
                                              where(model_password.Password.user_id == user_id,
                                                    model_password.Password.is_active))

        password = password.scalars().first()

        return password.hashed_password

    async def check_password(self, user_id: int, password_to_check: str) -> bool:
        """Check if the passed password is equal to the active password registered in database

        Parameters
        ----------
        user_id : int
            User's id that is going to be checked
        password_to_check : str
            password to be checked against the database

        Returns
        -------
        bool
            True if the password is correct, False if not
        """

        current_active_password = await self.get_active_password(user_id)
        hashed_password_to_check = model_password.Password.set_password(password_to_check)

        return current_active_password == hashed_password_to_check

    async def create_password(self, user_id: int, password: str,
                              expiration_date: date = None) -> model_password.Password:
        """Create a password only if there is no active password for the current user

        Parameters
        ----------
        user_id : int
            User that is going to be created the password
        password : str
            password to be set
        expiration_date : date, optional
            The expiration date for the password, by default None

        Returns
        -------
        model_password.Passwords
            Model Password object
        """

        if await self.there_is_active_password_for_user(user_id):
            raise HTTPException(status_code=400,
                                detail="there is already an active password. Use update_password method instead of "
                                       "create_password method")

        hashed_password = model_password.Password.set_password(password)

        db_password = model_password.Password(user_id=user_id,
                                              hashed_password=hashed_password,
                                              expiration_date=expiration_date)

        self.session.add(db_password)

        await self.session.flush()

        return db_password

    async def there_is_active_password_for_user(self, user_id: int) -> bool:
        """check if the user has an active password

        Parameters
        ----------
        db : Session
            Current SqlAlchemy database session
        user_id : int
            User's id that is wanted to get the current password


        Returns
        -------
        bool
            True if the user has an active password, False other way
        """

        rtn = await self.session.execute(select(model_password.Password).where(
            model_password.Password.user_id == user_id,
            model_password.Password.is_active))

        rtn = rtn.scalars().first()

        return rtn is not None

    async def update_password(self, user_id: int, current_password: str, new_password: str,
                              expiration_date: date = None) -> model_password.Password:
        """ Update the current password for the user

        Parameters
        ----------
        db : Session
            Current SqlAlchemy database session
        user_id : int
            User that is going to get a new password
        current_password : str
            password to be checked
        new_password : str
            new password for the user
        expiration_date : date, optional
            The espiration date for the password, by default None

        Returns
        -------
        model_password.Passwords
            Model Password object
        """

        if not await self.there_is_active_password_for_user(user_id):
            raise HTTPException(status_code=400,
                                detail="There is no an active password. Use create_password method instead of "
                                       "update_password method")

        if await self.check_password(user_id, current_password):
            # this make this function a non-pure function
            await self.disable_passwords(user_id)
            return await self.create_password(user_id, new_password, expiration_date)

        else:
            raise HTTPException(status_code=400,
                                detail="Password can not be changed. Current active password does not match with the "
                                       "'Current password given'")

    async def disable_passwords(self, user_id: int) -> int:
        """Disables all password for an user

        Parameters
        ----------
        user_id : int
            User that is going to be disabled

        Returns
        -------
        int
            User's id that is disabled
        """
        password = await self.session.execute(select(model_password.Password).
                                              where(model_password.Password.user_id == user_id,
                                                    model_password.Password.is_active))
        passwords = password.scalars().all()

        for pwd in passwords:
            pwd.is_active = False

        await self.session.flush()

        return user_id
