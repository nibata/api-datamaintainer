from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

import os,sys,inspect
 
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)


from dotenv import load_dotenv

load_dotenv(f"{parent_dir}/env/.env")

SQLALCHEMY_DATABASE_URL = os.environ.get("URI_DATABASE") 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
Base = declarative_base()
