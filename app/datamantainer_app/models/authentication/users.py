import hashlib
from ...configs.database import Base
from ...configs.settings import SECRET_KEY
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey, UniqueConstraint, false
 

# Tabla de relacion entre users y groups (muchos a muchos). la documentacion recomienda 
# encarecidamente no realizar esta relacion con un modelo si no que con una tabla directamente
users_groups = Table('users_groups',
                     Base.metadata,
                     Column('user_id', Integer, ForeignKey('authentication.users.id'), primary_key=True),
                     Column('group_id', Integer, ForeignKey('authentication.groups.id'), primary_key=True),    
                     UniqueConstraint('user_id', 'group_id', name='uix_1'),
                     schema = "authentication",) 


class Users(Base):
    """User Class contains standard information for a User."""
 
    __tablename__ = "users"
    __table_args__ = {"schema": "authentication"}

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, server_default=false(), nullable=False)
    address = Column(String)
    age = Column(Integer)

    users_groups = relationship('Groups', secondary=users_groups, lazy='subquery', backref=backref('users', lazy=True)) 

    '''
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
    '''
    '''
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
    '''       