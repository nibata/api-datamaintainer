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
from fastapi import FastAPI
from .configs import settings
from .routes import users_routes

app = FastAPI(
        title=settings.APP_NAME,
        description=settings.DESCRIPTION
)

app.include_router(users_routes.router)
