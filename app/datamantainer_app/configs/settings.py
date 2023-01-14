"""
Se deja la configuración inicial de la aplicación y se cargan las variables de entorno.
"""
import os, inspect
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)

load_dotenv(f"{root_dir}/env/.env")


APP_NAME = "DATAMANTAINER API"
DESCRIPTION="Aplicación API de prueba con mantenedor de base de datos mediante Alembic"
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL")
SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URL = os.environ.get("URI_DATABASE")
DEBUG = os.environ.get("DEBUG")
