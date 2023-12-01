from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.config import Config
from database.database import DB
from datetime import datetime

origins = [
"http://127.0.0.1:5173/"
]

class Server():

    def __init__(self, config:Config):
        self.__config:Config = config
        self.db = DB(config.DbConfig)
        self.app:FastAPI = FastAPI()
        self.start:datetime = datetime.utcnow()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins= origins,
            allow_credentials= True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    