import os
from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine
from config.config import Config
from models.product_model import Product
from schema.product_schema import Product_pydantic
from models.user_model import User
from schema.user_schema import User_pydantic
from models.rol_model import Rol
from schema.rol_schema import Rol_pydantic
from database.database import (
    OpenSession,
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
        result = session.query(Product).all()    
        print(result)
        return(result)
        
    
    @app.post("/products", response_model=Product_pydantic)
    async def create_product(prod : Product_pydantic):
        #Create a new product and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        session.add(newproduct)
        session.commit()
        CloseSession(session)
        return (prod)

    @app.post("/users", response_model=User_pydantic)
    async def create_user(user : User_pydantic):
        #Create a new user and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newuser = User(user.username, user.password, user.is_active,)
        session.add(newuser)
        session.commit()
        CloseSession(session)
        return(user)
    
    @app.post("/roles", response_model=Rol_pydantic)
    async def create_rol(rol : Rol_pydantic):
        config = Config()
        session = OpenSession(config.DbConfig)
        newrol = Rol(rol.rol)
        session.add(newrol)
        session.commit()
        CloseSession(session)
        return(rol)

def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    engine = create_engine(f"mysql+mysqlconnector://root:asdasd@127.0.0.1:3306/book_db")
    meta.create_all(engine)
    return app