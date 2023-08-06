from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from typing import List


if TYPE_CHECKING:
    from .users_groups import UserGroupLink


# BASE
class GroupBase(SQLModel):
    Code: str = Field(nullable=False, unique=True, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    Description: str


# TABLE
class Group(GroupBase, table=True):
    """Group Class contains standard information for a Groups."""

    __tablename__ = "Group"
    __table_args__ = {"schema": "Authentication"}

    Id: int = Field(nullable=False, primary_key=True)

    # Relations
    UserLinks: List["UserGroupLink"] = Relationship(back_populates="Groups")


# SCHEMAS
class GroupRead(GroupBase):
    Id: int


class GroupCreate(GroupBase):
    pass
