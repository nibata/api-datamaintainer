from ...auth import auth_bearer
from fastapi import APIRouter, Depends, HTTPException
from ...schemas.authentication import password_schema
from ...controller.authentication.users_controller import UsersController
from ...controller.authentication.passwords_controller import PasswordsController

from ...configs.database import SessionLocal


router = APIRouter()


@router.post("/password/create_password",
             response_model=password_schema.PasswordsBase,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["ADMINISTRATOR"]))])
async def create_password(form_user_pwd: password_schema.CreatePassword):
    async with SessionLocal() as session:
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
             response_model=password_schema.PasswordsBase,
             dependencies=[Depends(auth_bearer.JWTBearer(required_permission=["DEFAULT"]))])
async def update_password(form_user_pwd: password_schema.UpdatePassword):
    # Se fuerza que el usuario esté logeado al pedir como dependencia el rol DEFAULT, ya que para que el rol lo tienen
    # todos los usuarios que han ingresado mediante sus credenciales.
    async with SessionLocal() as session:
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
