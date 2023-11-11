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
    uri_async_db = os.environ.get("DB_ASYNC_TEST")
    DB_DRIVER = os.environ.get("DB_DRIVER")
    DB_ASYNC_DRIVER = os.environ.get("DB_ASYNC_DRIVER")
    DB_USER = os.environ.get("DB_USER")
    DB_PASS = os.environ.get("DB_PASS")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")
    DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
    SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}+{DB_ASYNC_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_NAME}"

    print("#" * 10)
    print("#" * 10)
    print("#" * 10)
    print(uri_async_db)
    print(SQLALCHEMY_DATABASE_URL)
    print("#" * 10)
    print("#" * 10)
    print("#" * 10)
    if uri_async_db is not None:
        engine = create_engine(uri_async_db)
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

    else:
        engi
