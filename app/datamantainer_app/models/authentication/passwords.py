from ...configs.settings import SECRET_KEY
from sqlmodel import SQLModel, Field
from datetime import datetime, date
from .users import User
import hashlib

from pydantic import EmailStr


class PasswordBase(SQLModel):
    CreationDate: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    IsActive: bool = Field(nullable=False, default=True)
    ExpirationDate: date = Field(nullable=True)


class Password(PasswordBase, table=True):
    """Password Class contains standard information for a Passwords for users."""
 
    __tablename__ = "Password"
    __table_args__ = {"schema": "Authentication"}

    Id: int = Field(primary_key=True, nullable=False)
    UserId: int = Field(foreign_key=User.Id)
    HashedPassword: str = Field(nullable=False, max_length=120)


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
    UserId: int
    IsActive: bool
    ExpirationDate: date


class PasswordUpdate(SQLModel):
    Email: EmailStr = Field(nullable=False)
    CurrentPassword: str = Field(nullable=False)
    NewPassword: str = Field(nullable=False)
    ExpirationDate: date = Field(nullable=True)


class PasswordCreate(SQLModel):
    Email: EmailStr = Field(nullable=False)
    Password: str = Field(nullable=False)
    ExpirationDate: date = Field(nullable=True)
