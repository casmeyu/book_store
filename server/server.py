import os
from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine

from database.database import (
    OpenConnection,
    OpenSession,
    CloseConnection,
    CloseSession,
    GetDatabaseTables,
    meta
)
from config.config import Config
from models.product_model import Product
from schema.product_schema import Product_pydantic

 
def setupServerRoutes(app:FastAPI):
    @app.get("/")
    async def root():
        return {"message": "Book store home page!"}

    @app.get("/api/db/tables")
    async def getDbTables():
        config = Config()
        session = OpenSession(config.DbConfig)
        db_tables = GetDatabaseTables(session)
        return db_tables
        
    @app.get("/products")
    async def getAllProducts():
        config = Config()
        conn = OpenConnection(config.DbConfig)
        print("JOJOJO")
        result = conn.execute(select(Product)).fetchall()
        print(result)
        
    

    @app.post("/products")
    async def create_product(prod : Product_pydantic):
        #Create a new product and save it in the database
        config = Config()
        conn = OpenConnection(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        print("123")
        result = conn.execute(insert(Product).values(name = prod.name, price = prod.price))
        conn.commit()
        print(result.lastrowid)
        lastrowid = result.lastrowid
        print("ok")


def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    engine = create_engine(f"mysql+mysqlconnector://root:asdasd@127.0.0.1:3306/book_db")
    meta.create_all(engine)
    return app