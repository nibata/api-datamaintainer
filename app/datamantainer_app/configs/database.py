from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from .settings import SQLALCHEMY_DATABASE_URL
from sqlmodel import SQLModel, create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker


engine = AsyncEngine(create_engine(SQLALCHEMY_DATABASE_URL, future=True, poolclass=NullPool))
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
