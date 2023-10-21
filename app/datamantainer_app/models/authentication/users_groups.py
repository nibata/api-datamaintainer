from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from .groups import Group
from .users import User


class UserGroupLink(SQLModel, table=True):
    __tablename__ = "user_group_link"
    __table_args__ = (UniqueConstraint("user_id", "group_id", name="unique_user_group_constraint"),
                      {"schema": "authentication"})

    # Fields
    user_id: int = Field(foreign_key=User.id, primary_key=True)
    group_id: int = Field(foreign_key=Group.id, primary_key=True)

    # Relations
    users: User = Relationship(back_populates="group_links")
    groups: Group = Relationship(back_populates="user_links")
