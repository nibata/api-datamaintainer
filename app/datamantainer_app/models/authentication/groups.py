from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from typing import List


if TYPE_CHECKING:
    from .users_groups import UserGroupLink


# BASE
class GroupBase(SQLModel):
    code: str = Field(nullable=False, unique=True, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    description: str = Field(nullable=True)


# TABLE
class Group(GroupBase, table=True):
    """Group Class contains standard information for a Groups."""

    __tablename__ = "group"
    __table_args__ = {"schema": "authentication"}

    id: int = Field(nullable=False, primary_key=True)

    # Relations
    user_links: List["UserGroupLink"] = Relationship(back_populates="groups")


# SCHEMAS
class GroupRead(GroupBase):
    id: int


class GroupCreate(GroupBase):
    pass
