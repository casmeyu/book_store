from fastapi import FastAPI
from config.config import Config
from database.database import DB
from datetime import datetime
from routers.user_routes import setupUserRoutes
from routers.product_routes import setupProductRoutes
from routers.sale_routes import setupSaleRoutes
from routers.role_routes import setupRoleRoutes


class Server():
    def __init__(self, config:Config):
        self.__config:Config = config
        self.db = DB(config.DbConfig)
        self.app:FastAPI = FastAPI()
        self.app.include_router(setupUserRoutes(self.db))
        self.app.include_router(setupProductRoutes(self.db))
        self.app.include_router(setupSaleRoutes(self.db))
        self.app.include_router(setupRoleRoutes(self.db))
        self.start:datetime = datetime.utcnow()
        

    