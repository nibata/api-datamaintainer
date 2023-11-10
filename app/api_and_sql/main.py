"""
        _ _           _                                      _ _                      
       (_| |         | |         ____                       (_| |                     
  _ __  _| |__   __ _| |_ __ _  / __ \  __ _ _ __ ___   __ _ _| |  ___ ___  _ __ ___  
 | '_ \| | '_ \ / _` | __/ _` |/ / _` |/ _` | '_ ` _ \ / _` | | | / __/ _ \| '_ ` _ \ 
 | | | | | |_) | (_| | || (_| | | (_| | (_| | | | | | | (_| | | || (_| (_) | | | | | |
 |_| |_|_|_.__/ \__,_|\__\__,_|\ \__,_|\__, |_| |_| |_|\__,_|_|_(_\___\___/|_| |_| |_|
                                \____/  __/ |                                         
                                       |___/                                          
 nibata@gmail.com
"""
from app.api_and_sql.routes.authentication import users_routes, groups_routes, passwords_routes
from app.api_and_sql.routes.stock import stock_moves_routes
from app.api_and_sql.routes.default import default_routes
from fastapi.middleware.cors import CORSMiddleware
from app.api_and_sql.configs.sentry import *
from app.api_and_sql.configs import settings
from fastapi import FastAPI


app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION
)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(users_routes.router)
app.include_router(default_routes.router)
app.include_router(groups_routes.router)
app.include_router(passwords_routes.router)
app.include_router(stock_moves_routes.router)
