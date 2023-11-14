from fastapi import FastAPI
from database.database import DB
from config.config import Config
from sqlalchemy import Connection, text, select, insert
from models.product_model import Product

class Server():
    def __init__(self, config:Config):
        self.__config:Config = config
        self.db = DB(config.DbConfig)
        self.app:FastAPI = FastAPI()
