from typing import List, Optional
from pydantic import BaseModel
 
 
class GroupBase(BaseModel):
    code: str


class Group(GroupBase):
    id: int
    description: str

    class Config:
        orm_mode = True


class GroupCreate(GroupBase):
    description: str
