from ...modules.humps_implementation_module import to_kebab
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from typing import List, Optional
from pydantic import EmailStr
from datetime import date


if TYPE_CHECKING:
    from .users_groups import UserGroupLink


# BASE
class UserBase(SQLModel):
    full_name: str = Field(nullable=False, regex="^[a-zA-Z0-9äöüÄÖÜáéíóúÁÉÍÓÚ ]*$")
    email: EmailStr = Field(nullable=False)

    class Config:
        alias_generator = to_kebab
        allow_population_by_field_name = True


# TABLES
class User(UserBase, table=True):
    """User Class contains standard information for a User."""
 
    __tablename__ = "user"
    __table_args__ = {"schema": "authentication",
                      "extend_existing": True}

    # Fields
    id: int = Field(nullable=False, primary_key=True)
    is_active: bool = Field(default=False, nullable=False)

    # Relations
    group_links: List["UserGroupLink"] = Relationship(back_populates="users")


class UserCreate(UserBase):
    password: str = Field(nullable=False)
    expiration_date: Optional[date] = None


class UserLogin(SQLModel):
    email: EmailStr = Field(nullable=False)
    password: str = Field(nullable=False)

    class Config:
        alias_generator = to_kebab
        allow_population_by_field_name = True
