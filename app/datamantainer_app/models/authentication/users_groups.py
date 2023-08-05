from sqlmodel import SQLModel, Field, Relationship
from .groups import Group
from .users import User


class UserGroupLink(SQLModel, table=True):
    __tablename__ = "UserGroupLink"
    __table_args__ = {"schema": "Authentication"}

    # Fields
    UserId: int = Field(foreign_key=User.Id, primary_key=True)
    GroupId: int = Field(foreign_key=Group.Id, primary_key=True)

    # Relations
    Users: User = Relationship(back_populates="GroupLinks")
    Groups: Group = Relationship(back_populates="UserLinks")
