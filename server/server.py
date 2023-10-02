import os
from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine
from config.config import Config
from models.product_model import Product
from schema.product_schema import Product_pydantic
from database.database import (
    OpenConnection,
    OpenSession,
    CloseConnection,
    CloseSession,
    GetDatabaseTables,
    meta
)

 
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
        session = OpenSession(config.DbConfig)
        print("JOJOJO")
        result = session.query(Product).all()    
        print(result)
        return(result)
        
    
    @app.post("/products", response_model=Product_pydantic)
    async def create_product(prod : Product_pydantic):
        #Create a new product and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        #result = conn.execute(insert(Product).values(name = prod.name, price = prod.price))
        result = session.add(newproduct)
        session.commit()
        print(result)
        CloseSession(session)
        print("ok")
        return (prod)


def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    engine = create_engine(f"mysql+mysqlconnector://root:asdasd@127.0.0.1:3306/book_db")
    meta.create_all(engine)
    return app