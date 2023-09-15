import os
from fastapi import FastAPI
from database.database import Open, Close
from config.config import Config
from sqlalchemy import Connection, text, select



def setupServerRoutes(app:FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

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