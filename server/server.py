import os
from fastapi import FastAPI
from database.database import DB
from config.config import Config
from sqlalchemy import Connection, text, select, insert
from models.Product import Product
from routes.routes import setupServerRoutes

class Server():
    def __init__(self, config:Config):
        self.__config:Config = config
        self.db = DB(config.DbConfig)
        self.app:FastAPI = FastAPI()
        setupServerRoutes(self)