from fastapi import FastAPI
from config.config import Config
from database.database import DB
from datetime import datetime

class Server():
    def __init__(self, config:Config):
        self.__config:Config = config
        self.db = DB(config.DbConfig)
        self.app:FastAPI = FastAPI()
        self.start:datetime = datetime.utcnow()

    