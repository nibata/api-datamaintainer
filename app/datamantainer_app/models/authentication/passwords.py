import hashlib
from ...configs.database import Base
from ...configs.settings import SECRET_KEY
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, true, sql, Date

from .users import Users
 
 
class Passwords(Base):
    """Password Class contains standard information for a Passwords for users."""
 
    __tablename__ = "passwords"
    __table_args__ = {"schema": "authentication"}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey(Users.id), nullable=False)
    hashed_password = Column(String(120), nullable=False)
    creation_date = Column(DateTime, server_default=sql.func.now(), nullable=False)
    expiration_date = Column(Date)
    is_active = Column(Boolean, server_default=true(), nullable=False)


    @staticmethod
    def set_password(pwd: str) -> str:
        """Genera password hasheada mediante método md5

        Parameters
        ----------
        pwd : str
            Password a hashear

        Returns
        -------
        str
            Password hasheada
        """
        
        salt = SECRET_KEY
        password_to_hash = pwd + salt
        password = hashlib.md5(password_to_hash.encode()).hexdigest()

        return password
    