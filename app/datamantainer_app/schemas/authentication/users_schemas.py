from datetime import date
from pydantic import BaseModel
from typing import List, Optional
 
 
class UserBase(BaseModel):
    fullname: str
    email: str
 
 
class UserCreate(UserBase):
    password: str
    expiration_date: date = None
 

class User(UserBase):
    id: int
    is_active: bool
 
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
