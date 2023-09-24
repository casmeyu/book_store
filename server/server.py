import os

from fastapi import FastAPI
from database.database import Open, Close
from config.config import Config
from sqlalchemy import Connection, text, select, insert
from models.Product import Product, Product_pydantic


def setupServerRoutes(app:FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Book store home page!"}

    @app.get("/products")
    async def getAllProducts(prod : Product_pydantic):
        config = Config()
        conn = Open(config.DbConfig)
        print("JOJOJO")
        return conn.execute(Product_pydantic.select()).fetchall()


    @app.post("/products")
    async def createProducts(prod : Product_pydantic):
        #Create a new product and save it in the database
        print(prod)
        config = Config()
        conn = Open(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        print(newproduct)
        conn.execute(insert(Product).values(name = prod.name, price = prod.price))
        conn.commit()
        Close(conn)

def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    return app