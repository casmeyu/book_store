import os
from fastapi import FastAPI
from database.database import (
    OpenConnection,
    OpenSession,
    CloseConnection,
    CloseSession,
    GetDatabaseTables
)
from config.config import Config
from sqlalchemy import Connection, text, select



def setupServerRoutes(app:FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

    @app.get("/api/db/tables")
    async def getDbTables():
        config = Config()
        session = OpenSession(config.DbConfig)
        db_tables = GetDatabaseTables(session)
        return db_tables
        
    @app.get("/users")
    async def getAllUsers():
        config = Config()
        pass

    @app.post("/users")
    async def createUser():
        #Create a new user and save it in the database
        pass

def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    return app