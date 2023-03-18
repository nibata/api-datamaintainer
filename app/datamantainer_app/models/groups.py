from ..configs.database import Base
from sqlalchemy import Column, Integer, String 
 
 
class Groups(Base):
    """Groups Class contains standard information for a Groups."""
 
    __tablename__ = "groups"
    __table_args__ = {"schema": "authentication"}

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
    description = Column(String, unique=True, index=True)
