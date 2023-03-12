# API
Este proyecto está diseñado para mantener una base de datos mediante FastAPI y alembic.

Dentro de los primeros pasos se crea el proyecto que se menciona en el siguiente articulo: [ARTICULO](https://neuralcovenant.com/2020/12/29/aprendiendo-fastapi-con-postgresql/)

Para correr el proyecto con **gunicorn** ejecutar *(se deben usar workers uvicorn para esto)*: 
 - `gunicorn datamantainer_app.main:app --worker-class uvicorn.workers.UvicornWorker --reload`

Para crear las migraciones: 
 - `alembic revision --autogenerate -m "[MENSAJE]"`
 - `alembic upgrade head`

Para correr test unitarios sobre la API se requiere pytest y correr el comando `pytest` el cual ejecutará todos los test que encuentre en el proyecto. En el caso específico de este proyecto, los test se encuentran en la carpeta test de la aplicación.
