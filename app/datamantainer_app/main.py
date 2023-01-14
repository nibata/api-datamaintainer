from fastapi import FastAPI
from .routes import users as router_user

app = FastAPI()

app.include_router(router_user.router)
