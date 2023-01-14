from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .settings import SQLALCHEMY_DATABASE_URL
from sqlalchemy.ext.declarative import declarative_base

# Se da de alta la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
