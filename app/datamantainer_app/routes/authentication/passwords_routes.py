from ...models.authentication.passwords import PasswordRead, PasswordCreate, PasswordUpdate
from ...controller.authentication.passwords_controller import PasswordsController
from ...controller.authentication.users_controller import UsersController
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ...configs.database import get_session
from ...auth import auth_bearer


router = APIRouter()


@router.post("/password/create_password",
             response_model=PasswordRead,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def create_password(form_user_pwd: PasswordCreate, session: AsyncSession = Depends(get_session)):
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)

        db_user = await user_controller.get_user_by_email(email=form_user_pwd.Email)

        if not db_user:
            raise HTTPException(status_code=400, detail="Email does not exists")

        # set password
        db_password = await password_controller.create_password(user_id=db_user.Id,
                                                                password=form_user_pwd.Password,
                                                                expiration_date=form_user_pwd.ExpirationDate)

        session.expunge_all()

        return db_password


@router.post("/password/update_password",
             response_model=PasswordRead,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["DEFAULT"]))])
async def update_password(form_user_pwd: PasswordUpdate, session: AsyncSession = Depends(get_session)):
    # Se fuerza que el usuario esté logeado al pedir como dependencia el rol DEFAULT, ya que para que el rol lo tienen
    # todos los usuarios que han ingresado mediante sus credenciales.
    #async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)

        db_user = await user_controller.get_user_by_email(email=form_user_pwd.Email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Email does not exists")

        # set password
        db_password = await password_controller.update_password(user_id=db_user.Id,
                                                                current_password=form_user_pwd.CurrentPassword,
                                                                new_password=form_user_pwd.NewPassword,
                                                                expiration_date=form_user_pwd.ExpirationDate)

        session.expunge_all()

        return db_password
