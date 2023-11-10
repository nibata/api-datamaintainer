from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint
from ...modules.humps_implementation_module import to_kebab
from .groups import Group
from .users import User


class UserGroupLink(SQLModel, table=True):
    __tablename__ = "user_group_link"
    __table_args__ = (UniqueConstraint("user_id", "group_id", name="unique_user_group_constraint"),
                      {"schema": "authentication",
                       "extend_existing": True})

    # Fields
    user_id: int = Field(foreign_key=User.id, primary_key=True)
    group_id: int = Field(foreign_key=Group.id, primary_key=True)

    # Relations
    users: User = Relationship(back_populates="group_links")
    groups: Group = Relationship(back_populates="user_links")

    class Config:
        alias_generator = to_kebab
        allow_population_by_field_name = True
