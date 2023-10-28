import os
from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine, exists
from config.config import Config
from models.product_model import Product
from schema.product_schema import Product_pydantic
from models.user_model import User
from models.Venta import Venta
from schema.venta_schema import NewVentaSchema
from schema.user_schema import User_pydantic, NewUser, PublicUserInfo
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

    @app.post("/users", response_model=PublicUserInfo)
    async def create_user(user : NewUser):
        #Create a new user and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newuser = User(user.username, user.password, True)
        result = session.add(newuser)
        print ("RESULT", result)
        session.commit()
        userInfo = {
            username: user.username
        }
        CloseSession(session)
        return(userInfo)


    # Ventas
    @app.get("/ventas")
    async def getAllVentas():
        config = Config()
        session = OpenSession(config.DbConfig)
        res = session.query(Venta)
        print(res)
        CloseSession(session)
        return res

    @app.post("/ventas", response_model=NewVentaSchema)
    async def createVenta(ventaInfo: NewVentaSchema):
        config = Config()
        products = []

        session = OpenSession(config.DbConfig)
        
        # Check product existance in DB
        product_ids = [p.id for p in ventaInfo.products]
        print("Product ids", product_ids)
        db_products = session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            print("ERROR no estan los products")
        
        # Check user in the DB
        if (not session.query(exists().where(User.id == ventaInfo.user_id))):
            print("User does not exist")
        # Products are in DB
        new_venta = Venta()
        return (ventaInfo)

        # session.add(newVenta)
        # Anadir relaciones con productos
        # session.commit()
        # CloseSession(session)
        # return(newVenta)

def createServer():
    app = FastAPI()
    setupServerRoutes(app)
    engine = create_engine(f"mysql+mysqlconnector://casmeyu:qwe123@127.0.0.1:3306/book_store")
    meta.create_all(engine)
    return app