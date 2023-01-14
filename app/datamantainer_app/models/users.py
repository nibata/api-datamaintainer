from ..database import Base
#from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, Integer, String # , ForeignKey
 
 
class Users(Base):
    """User Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}
 
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(120))
    is_active = Column(Boolean, default=False)
    address = Column(String)
    age = Column(Integer)
