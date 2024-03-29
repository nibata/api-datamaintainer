"""
Se deja la configuración inicial de la aplicación y se cargan las variables de entorno.
"""
from dotenv import load_dotenv
import inspect
import os


current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

load_dotenv(f"{root_dir}/env/.env")


APP_NAME = "DATAMANTAINER API"
DESCRIPTION = "Aplicación API de prueba con mantenedor de base de datos mediante Alembic"
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
SECRET_KEY = os.environ.get("SECRET_KEY")
DB_DRIVER = os.environ.get("DB_DRIVER")
DB_ASYNC_DRIVER = os.environ.get("DB_ASYNC_DRIVER")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_DATABASE_NAME = os.environ.get("DB_DATABASE_NAME")
SQLALCHEMY_DATABASE_URL = f"{DB_DRIVER}+{DB_ASYNC_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_NAME}"

UNIT_TEST = os.environ.get("UNIT_TEST") == "True"
DB_ASYNC_TEST = os.environ.get("DB_ASYNC_TEST")
if UNIT_TEST:  # pragma: no cover
    SQLALCHEMY_DATABASE_URL = DB_ASYNC_TEST

DEBUG = os.environ.get("DEBUG")
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
USER_ADMIN = os.environ.get("USER_ADMIN")
PASS_ADMIN = os.environ.get("PASS_ADMIN")
SENTRY_DNS = os.environ.get("SENTRY_DNS")
CRYPTO_KEY = os.environ.get("CRYPTO_KEY").encode()
