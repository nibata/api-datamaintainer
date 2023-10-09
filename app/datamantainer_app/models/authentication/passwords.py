from ...configs.settings import SECRET_KEY
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from pydantic import EmailStr
from typing import Optional
from .users import User
import hashlib


class PasswordBase(SQLModel):
    creation_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(nullable=False, default=True)
    expiration_date: Optional[date] = Field(nullable=True)


class Password(PasswordBase, table=True):
    """Password Class contains standard information for a Passwords for users."""
 
    __tablename__ = "password"
    __table_args__ = {"schema": "authentication"}

    id: int = Field(primary_key=True, nullable=False)
    user_id: int = Field(foreign_key=User.id)
    hashed_password: str = Field(nullable=False, max_length=120)


    @staticmethod
    def set_password(pwd: str) -> str:
        """Genera password hasheada mediante método md5

        Parameters
        ----------
        pwd : str
            Password a hashear

        Returns
        -------
        str
            Password hasheada
        """
        
        salt = SECRET_KEY
        password_to_hash = pwd + salt
        password = hashlib.md5(password_to_hash.encode()).hexdigest()

        return password


class PasswordRead(SQLModel):
    user_id: int
    is_active: bool
    expiration_date: Optional[date] = None


class PasswordUpdate(SQLModel):
    email: EmailStr = Field(nullable=False)
    current_password: str = Field(nullable=False)
    new_password: str = Field(nullable=False)
    expiration_date: Optional[date] = None


class PasswordCreate(SQLModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)
    expiration_date: Optional[date] = None
