from ...modules.humps_implementation_module import to_kebab
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from typing import List


if TYPE_CHECKING:
    from .users_groups import UserGroupLink  # pragma: no cover


# BASE
class GroupBase(SQLModel):
    code: str = Field(nullable=False, unique=True, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    description: str = Field(nullable=True)

    class Config:
        alias_generator = to_kebab
        allow_population_by_field_name = True


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
