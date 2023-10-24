import os
from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine
from sqlalchemy.orm import joinedload
from config.config import Config
from models.product_model import Product
from schema.product_schema import Product_pydantic
from models.user_model import User, user_role
from schema.user_schema import User_pydantic
from models.user_model import Rol
from schema.rol_schema import Rol_pydantic
from passlib.context import CryptContext
import datetime
from database.database import (
    OpenSession,
    CloseSession,
    GetDatabaseTables,
    meta,
    Hasher
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
    
    @app.get("/products/{product_id}", response_model=Product_pydantic)
    async def get_product_by_id(prod : Product_pydantic):
        config = Config()
        session = OpenSession(config.DbConfig)
        product_by_id = Product(prod.name, prod.price)
        session.get

        
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
        new_user = User(user.username, user.password, user.created_at, user.is_active)
        #password hash
        hash_password = Hasher.get_hash_password(new_user.password)
        new_user.password = hash_password
        #created_at
        new_user.created_at = datetime.datetime.now()
        dbRoles = session.query(Rol.id).filter(Rol.id.in_(user.roles)).all()
        if len(dbRoles) != len(user.roles):
            print("ERROR FATAL LOS ROLES ESTAN MAL")
            return "error with roles"
        session.add(new_user)
        db_user:User = session.query(User.id).where(User.username == user.username).first() # Grab user from db
        for r in user.roles:
            session.execute(user_role.insert().values(user_id=db_user.id, role_id=r))
        session.commit()
        CloseSession(session)
        return(user)
    
    @app.post("/roles", response_model=Rol_pydantic)
    async def create_rol(rol : Rol_pydantic):
        #Create a new rol and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newrol = Rol(rol.name)
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