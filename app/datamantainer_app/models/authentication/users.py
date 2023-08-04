from ...configs.database import Base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey, UniqueConstraint, false


# Tabla de relación entre users y groups (muchos a muchos). La documentación recomienda
# encarecidamente no realizar esta relación con un modelo sino que con una tabla directamente
users_groups = Table('users_groups',
                     Base.metadata,
                     Column('user_id', Integer, ForeignKey('authentication.users.id'), primary_key=True),
                     Column('group_id', Integer, ForeignKey('authentication.groups.id'), primary_key=True),    
                     UniqueConstraint('user_id', 'group_id', name='uix_1'),
                     schema="authentication",)


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
