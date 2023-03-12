import hashlib
from ..configs.database import Base
#from sqlalchemy.orm import relationship
from ..configs.settings import SECRET_KEY
from sqlalchemy import Boolean, Column, Integer, String # , ForeignKey
 
 
class Users(Base):
    """User Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(120))
    is_active = Column(Boolean, default=False)
    address = Column(String)
    age = Column(Integer)

    
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

        # TODO: agregarle salt proveniente de las variables de entorno para aumentar seguridad de password
        
        salt = SECRET_KEY
        password_to_hash = pwd + salt
        password = hashlib.md5(password_to_hash.encode()).hexdigest()

        return password


    def check_password(self, pwd: str) -> bool:
        """Chequea que el password se corresponda con lo registrado en base de datos.

        Parameters
        ----------
        pwd : str
            Password a chequear

        Returns
        -------
        bool
            True si la password ingresada se corresponde con el usuario, False en caso contrario.
        """
        salt = SECRET_KEY
        password_to_hash = pwd + salt
        password = hashlib.md5(password_to_hash.encode()).hexdigest()

        check = password == self.hashed_password

        return check
        
        
