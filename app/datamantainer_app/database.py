import os, inspect
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)

load_dotenv(f"{parent_dir}/env/.env")

# Importante tene URI_DATABASE definido como variable de entorno
SQLALCHEMY_DATABASE_URL = os.environ.get("URI_DATABASE") 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
