from ...models.authentication.passwords import PasswordRead, PasswordCreate, PasswordUpdate, PasswordDeactivate
from ...controller.authentication.passwords_controller import PasswordsController
from ...controller.authentication.users_controller import UsersController
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from ...configs.database import get_session
from ...auth import auth_bearer


router = APIRouter()


@router.post("/password/create_password",
             response_model=PasswordRead,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))],
             tags=["Authentication"])
async def create_password(form_user_pwd: PasswordCreate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)

        db_user = await user_controller.get_user_by_email(email=form_user_pwd.email)

        if not db_user:
            raise HTTPException(status_code=400, detail="Email does not exists")

        # set password
        db_password = await password_controller.create_password(user_id=db_user.id,
                                                                password=form_user_pwd.password,
                                                                expiration_date=form_user_pwd.expiration_date)

        session.expunge_all()

        return db_password


@router.post("/password/update_password",
             response_model=PasswordRead,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["DEFAULT"]))],
             tags=["Authentication"])
async def update_password(form_user_pwd: PasswordUpdate, session: AsyncSession = Depends(get_session)):
    # Se fuerza que el usuario esté logeado al pedir como dependencia el rol DEFAULT, ya que para que el rol lo tienen
    # todos los usuarios que han ingresado mediante sus credenciales.
    # async with SessionLocal() as session:
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)

        db_user = await user_controller.get_user_by_email(email=form_user_pwd.email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Email does not exists")

        # set password
        db_password = await password_controller.update_password(user_id=db_user.id,
                                                                current_password=form_user_pwd.current_password,
                                                                new_password=form_user_pwd.new_password,
                                                                expiration_date=form_user_pwd.expiration_date)

        session.expunge_all()

        return db_password


@router.post("/password/deactivate_password",
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))],
             tags=["Authentication"])
async def deactivate_password(form_user_pwd: PasswordDeactivate, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        user_controller = UsersController(session)
        password_controller = PasswordsController(session)

        db_user = await user_controller.get_user_by_email(email=form_user_pwd.email)
        if not db_user:
            raise HTTPException(status_code=400, detail="Email does not exists")

        db_password = await password_controller.disable_passwords(user_id=db_user.id)

        session.expunge_all()

        return {"msg": f"Password para {form_user_pwd.email} se ha desactivado correctamente."}
