from datetime import date
from pydantic import BaseModel
from typing import List, Optional
 
 
class UserBase(BaseModel):
    email: str
 
 
class UserCreate(UserBase):
    fullname: str
    password: str
    expiration_date: date = None
 

class User(UserBase):
    id: int
    is_active: bool
    fullname: str
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: str
    password: str
