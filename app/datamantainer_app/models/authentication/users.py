from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from datetime import date
from typing import List


if TYPE_CHECKING:
    from .users_groups import UserGroupLink


# BASE
class UserBase(SQLModel):
    FullName: str = Field(nullable=False, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    Email: str = Field(nullable=False, regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$")


# TABLES
class User(UserBase, table=True):
    """User Class contains standard information for a User."""
 
    __tablename__ = "User"
    __table_args__ = {"schema": "Authentication"}

    # Fields
    Id: int = Field(nullable=False, primary_key=True)
    IsActive: bool = Field(default=False, nullable=False)

    # Relations
    GroupLinks: List["UserGroupLink"] = Relationship(back_populates="Users")


class UserCreate(UserBase):
    Password: str = Field(nullable=False)
    ExpirationDate: date = Field(nullable=True)


class UserLogin(SQLModel):
    Email: str = Field(nullable=False, regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$")
    Password: str = Field(nullable=False)
