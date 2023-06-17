from datetime import date
from pydantic import BaseModel
from typing import List, Optional
 
 
class PasswordsBase(BaseModel):
    expiration_date: date
    user_id: int
    
    class Config:
        orm_mode = True
        

class UpdatePassword(BaseModel):
    email: str
    current_password: str
    new_password: str
    expiration_date: date = None


class CreatePassword(BaseModel):
    email: str
    password: str
    expiration_date: date = None
