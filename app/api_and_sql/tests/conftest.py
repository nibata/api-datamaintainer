from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from alembic.config import Config
from alembic import command
import pytest
import os


# Database setup
@pytest.fixture(scope="session")
def db():
    # Create a test database engine
    uri_async_db = os.environ.get("DB_ASYNC_TEST")
    engine = create_engine(uri_async_db)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Run Alembic migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("script_location", "alembic")
    # I couldn't make it work with an async url, doesn't matter due I don't really need it
    # in the upgrade of the database
    command.upgrade(alembic_cfg, "head")

    # Create a new session for the tests
    session = Session()

    yield session

    # Teardown: Drop the test database
    session.close()
    engine.dispose()
    command.downgrade(alembic_cfg, "base")