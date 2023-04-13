# API
Este proyecto está diseñado para mantener una base de datos mediante FastAPI y alembic.

Dentro de los primeros pasos se crea el proyecto que se menciona en el siguiente articulo: [ARTICULO](https://neuralcovenant.com/2020/12/29/aprendiendo-fastapi-con-postgresql/)

Para correr el proyecto con **gunicorn** ejecutar *(se deben usar workers uvicorn para esto)*: 
 - `gunicorn datamantainer_app.main:app --worker-class uvicorn.workers.UvicornWorker --reload`

Para correr directamente con **uvicorn** (en el caso de usar Windows):
 - `uvicorn datamantainer_app.main:app --reload`

Para crear las migraciones: 
 - `alembic revision --autogenerate -m "[MENSAJE]"`
 - `alembic upgrade head`

Para correr test unitarios sobre la API se requiere pytest y correr el comando `pytest` el cual ejecutará todos los test que encuentre en el proyecto. En el caso específico de este proyecto, los test se encuentran en la carpeta test de la aplicación.


## Variables de entorno
Se está utilizando **dotenv** para trabajar y esta buscando el archivo `.env` en la siguiente ruta:
`app/env/.env`

Las variables a utilizar son:

 - SECRET_KEY: usar cualquier cosa que se acomode a las necesidades del desarrollo
 - ADMIN_EMAIL: usar el mail que se acomode
 - DEBUG: True o False
 - DB_DRIVER: Nombre del driver compatible con sqlalchemy
 - DB_USER: Nombre del usuario de la base de datos
 - DB_PASS: Clave del usuario de la base de datos
 - DB_HOST: Host o ip de la base de datos
 - DB_PORT: Puerto de la base de datos
 - DB_DATABASE_NAME: Nombre de la base de datos (al utilizar alembic se creará una base de datos con este nombre)
 - JWT_SECRET: Clave secreta JWT (Rellenar con lo que se estime conveniente)
 - JWT_ALGORITHM: algoritmo JWT de encriptación (ej: HS256)
 - USER_ADMIN: mail del usuario administrador que se creará en la base de datos una vez creada la tabla de usuarios
 - PASS_ADMIN: password de dicho usuario administrador
 - SENTRY_DNS: Por si se está utilizando SENTRY, acá se debe colocar la DNS entregada por el servicio