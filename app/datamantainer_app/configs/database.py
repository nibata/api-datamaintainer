from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .settings import SQLALCHEMY_DATABASE_URL, USE_ASYNC
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

# Se da de alta la base de datos
if USE_ASYNC:
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, poolclass=NullPool)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
 
Base = declarative_base()
