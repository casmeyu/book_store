from fastapi import FastAPI
from sqlalchemy import select, insert, create_engine, exists
from config.config import Config
from models.Venta import Venta, Product
from schema.product_schema import ProductSchema
from models.user_model import User, user_role
from schema.user_schema import User_pydantic, NewUser, PublicUserInfo
from models.user_model import Rol
from schema.rol_schema import Rol_pydantic

from schema.venta_schema import VentaSchema, NewVentaRequest, FinalProductOrder
from models.book_model import Book
from schema.book_schema import Book_pydantic
from datetime import datetime
from database.database import *

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
    
    @app.get("/products/{product_id}", response_model=ProductSchema)
    async def get_product_by_id():
        config = Config()
        session = OpenSession(config.DbConfig)
        product_by_id = session
        session.get

    @app.get("/books")
    async def getAllBooks():
        config = Config()
        session = OpenSession(config.DbConfig)
        result = session.query(Book).all()    
        print(result)
        return(result)

    @app.post("/products", response_model=ProductSchema)
    async def create_product(prod : ProductSchema):
        #Create a new product and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        session.add(newproduct)
        session.commit()
        CloseSession(session)
        return (prod)

    @app.get("/users", response_model=list[PublicUserInfo])
    async def get_all_users():
        config = Config()
        session = OpenSession(config.DbConfig)
        allUsers = session.query(User).all()
        # Convert all users to PublicUserInfo (pydantic)
        publicUsers = [PublicUserInfo.from_orm(u) for u in allUsers]
        return(publicUsers)

    @app.post("/users", response_model=PublicUserInfo)
    async def create_user(user : NewUser):
        config = Config()
        session = OpenSession(config.DbConfig)
        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        db_roles = session.query(Rol).filter(Rol.id.in_(user.roles)).all()
        #ver documentacion pydantic response model error
        #Check roles existance
        if len(db_roles) != len(user.roles):
            print("ERROR FATAL LOS ROLES ESTAN MAL")
            return PublicUserInfo(username="No hay roles mi amigo", is_active=False)
        
        new_user.roles = db_roles

        session.add(new_user)
        db_user:User = session.query(User).where(User.username == user.username).first() # Grab user from db
        # for r in user.roles:
        #     session.execute(user_role.insert().values(user_id=db_user.id, role_id=r))
        session.commit()

        publicUser = PublicUserInfo.from_orm(db_user)
        
        CloseSession(session)
        return(publicUser)


    # Ventas
    @app.get("/ventas")
    async def getAllVentas():
        config = Config()
        session = OpenSession(config.DbConfig)
        ventas = session.query(Venta).all()
        ventas = [VentaSchema.from_orm(v) for v in ventas]
        CloseSession(session)
        return ventas

    @app.post("/ventas", response_model=NewVentaRequest)
    async def createVenta(ventaInfo: NewVentaRequest):
        config = Config()
        products = []

        session = OpenSession(config.DbConfig)
        
        # Check product existance in DB
        product_ids = [p.id for p in ventaInfo.products]
        print("Product ids", product_ids)
        db_products = session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            print("ERROR no estan los products")
        # Products are in DB
        # Check user in the DB
        if (not session.query(exists().where(User.id == ventaInfo.user_id))):
            print("User does not exist")
        
        product_list = []

        for p in ventaInfo.products:
            item = {
                "quantity": p.quantity
            }
            for db_p in db_products:
                if (p.id == db_p.id):
                    print("Encontre el producto")
                    item["product"] = db_p
                    product_list.append(item)

        print("LISTA FINAL DE PRODUCTOS COMBINADA")
        print(product_list)

        new_venta = Venta(ventaInfo.user_id, product_list)
        print("NEW VENTA IS")
        print(new_venta)
        

        session.add(new_venta)
        session.commit()
        CloseSession(session)
        return(ventaInfo)
        
    
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
    
    @app.post("/books", response_model=Book_pydantic)
    async def create_book(book : Book_pydantic):
        #Create a new book and save it in the database
        config = Config()
        session = OpenSession(config.DbConfig)
        newbook = Book(book.isbn, book.title, book.author, book.publisher, book.price)
        session.add(newbook)
        session.commit()
        CloseSession(session)
        return(book)

def createServer():
    config = Config()
    app = FastAPI()
    setupServerRoutes(app)
    MakeMigration(config.DbConfig)
    return app

