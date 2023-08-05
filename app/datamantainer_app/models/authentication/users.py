from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from .users_groups import UserGroupLink


# BASE
class UserBase(SQLModel):
    FullName: str = Field(nullable=False, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    Email: str = Field(nullable=False, regex="^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
    IsActive: bool = Field(default=False, nullable=False)


# TABLES
class User(UserBase, table=True):
    """User Class contains standard information for a User."""
 
    __tablename__ = "User"
    __table_args__ = {"schema": "Authentication"}

    Id: int = Field(nullable=False, primary_key=True)
    GroupLinks: List["UserGroupLink"] = Relationship(back_populates="Users")
