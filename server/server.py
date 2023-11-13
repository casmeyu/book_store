from fastapi import FastAPI
from database.database import DB
############3
from sqlalchemy import select, insert, create_engine, exists
from sqlalchemy.orm import joinedload
##########3333
from config.config import Config
from models.Venta import Venta, Product, venta_product
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

    # @app.get("/api/db/tables")
    # async def getDbTables():
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
    #     db_tables = GetDatabaseTables(session)
    #     return db_tables
        
    @app.get("/products")
    async def getAllProducts():
        config = Config()
        db = DB(config.DbConfig)
        result = db.session.query(Product).all()
        return(result)
    
    @app.get("/products/{product_id}", response_model=ProductSchema)
    async def get_product_by_id():
        config = Config()
        db = DB(config.DbConfig)
        product = db.session.query(Product).get(product_id)
        return product

    # @app.get("/books")
    # async def getAllBooks():
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
    #     result = session.query(Book).all()    
    #     print(result)
    #     return(result)

    # @app.post("/products", response_model=ProductSchema)
    # async def create_product(prod : ProductSchema):
    #     #Create a new product and save it in the database
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
    #     newproduct = Product(prod.name, prod.price)
    #     session.add(newproduct)
    #     session.commit()
    #     CloseSession(session)
    #     return (prod)

    @app.get("/users/{user_id}", response_model=PublicUserInfo)
    async def get_user_by_id():
        config = Config()
        db = DB(config.DbConfig)
        user = db.session.query(User).get(user_id)
        public_user = PublicUserInfo.from_orm(user)
        return public_user

    @app.get("/users", response_model=list[PublicUserInfo])
    async def get_all_users():
        config = Config()
        db = DB(config.DbConfig)
        allUsers = db.session.query(User).all()
        # Convert all users to PublicUserInfo (pydantic)
        publicUsers = [PublicUserInfo.from_orm(u) for u in allUsers]
        return(publicUsers)

    @app.post("/users", response_model=PublicUserInfo)
    async def create_user(user : NewUser):
        config = Config()
        db = DB(config.DbConfig)

        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        db_roles = db.session.query(Rol).filter(Rol.id.in_(user.roles)).all()
        #ver documentacion pydantic response model error
        #Check roles existance only by length comparation
        if len(db_roles) != len(user.roles):
            #HANDLE ERRORS HANDLE ERRORS
            print("ERROR FATAL FALTAN O SOBRAN ROLES")
            return PublicUserInfo(username="ALGO MAL CON LOS ROLES AMIGO", is_active=False)
            
        new_user.roles = db_roles

        db.session.add(new_user)
        db.session.flush()
        db.session.refresh(new_user)
        db.session.commit()
        db.CloseSession()

        publicUser = PublicUserInfo.from_orm(new_user)
        return(publicUser)

    # # Ventas
    # @app.get("/ventas")
    # async def getAllVentas():
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
    #     ventas = session.query(Venta).options(joinedload(Venta.products)).all()
    #     CloseSession(session)
    #     return ventas

    # @app.post("/ventas", response_model=NewVentaRequest)
    # async def createVenta(ventaInfo: NewVentaRequest):
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
        
    #     # Check product existance in DB
    #     product_ids = [p.id for p in ventaInfo.products]
    #     db_products = session.query(Product).filter(Product.id.in_(product_ids)).all()
    #     if (len(product_ids) != len(db_products)):
    #         print("ERROR no estan los products")
    #         # HANDLE ERRORS HANDLE ERRORS
        
    #     # Check user in the DB
    #     if (not session.query(exists().where(User.id == ventaInfo.user_id))):
    #         print("User does not exist")
    #         # HANDLE ERRORS HANDLE ERRORS
        
    #     # Calculating final price and getting the products into product_list
    #     product_list = []
    #     venta_price = 0.0

    #     # THIS SHOULD BE CHANGED TO A HASH TABLE INSTEAD OF NESTED FOR LOOPS
    #     # ALSO THERE IS POSIBBLE ERROR IF I SEND THE SAME ITEM TWICE IN THE VENTA REQUEST
    #     # This error will be fixed with the hash table but it is a minor thing as of now
    #     for p in ventaInfo.products:
    #         item = {
    #             "quantity": p.quantity
    #         }
    #         for db_p in db_products:
    #             if (p.id == db_p.id):
    #                 item["product"] = db_p
    #                 product_list.append(item)
    #                 venta_price += p.quantity * db_p.price

    #     new_venta = Venta(ventaInfo.user_id, venta_price)
    #     session.add(new_venta)
    #     session.flush()
    #     session.refresh(new_venta)
        
    #     # Add the venta_product relationshinp
    #     #Here we have another loop
    #     for item in product_list:
    #         print("Adding ", item["product"].name)
    #         session.execute(venta_product.insert().values(
    #             venta_id=new_venta.id,
    #             product_id=item["product"].id,
    #             quantity=item["quantity"],
    #             price=item["product"].price
    #             )
    #         )
    #     session.commit()
    #     CloseSession(session)
    #     return(ventaInfo)
        
    
    @app.post("/roles", response_model=Rol_pydantic)
    async def create_rol(rol: Rol_pydantic):
        #Create a new rol and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        newrol = Rol(rol.name)
        db.session.add(newrol)
        db.session.commit()
        db.CloseSession()
        return(rol)
    
    # @app.post("/books", response_model=Book_pydantic)
    # async def create_book(book : Book_pydantic):
    #     #Create a new book and save it in the database
    #     config = Config()
    #     session = OpenSession(config.DbConfig)
    #     newbook = Book(book.isbn, book.title, book.author, book.publisher, book.price)
    #     session.add(newbook)
    #     session.commit()
    #     CloseSession(session)
    #     return(book)

    @app.get("/open")
    async def open():
        config = Config()
        db = DB(config.DbConfig)
        res = db.GetDatabaseTables()
        print(res)

def createServer():
    config = Config()
    app = FastAPI()
    setupServerRoutes(app)
    db = DB(config.DbConfig)
    db.MakeMigration()
    return app

