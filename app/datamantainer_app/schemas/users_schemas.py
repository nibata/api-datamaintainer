from typing import List, Optional
from pydantic import BaseModel
 
 
class UserBase(BaseModel):
    fullname: str
    email: str
 
 
class UserCreate(UserBase):
    password: str
 
 
class User(UserBase):
    id: int
    is_active: bool
 
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str

