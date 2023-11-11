import os
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine

from alembic import context


# Database setup
@pytest.fixture(scope="session")
def db():
    # Create a test database engine
    engine = create_engine("postgresql+asyncpg://postgres:postgrespw@localhost:55000/FastAPI_DB_Test")
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    command.upgrade(alembic_cfg, "head")

    # Create a new session for the tests
    session = Session()

    yield session

    # Teardown: Drop the test database
    session.close()
    engine.dispose()
    command.downgrade(alembic_cfg, "base")
