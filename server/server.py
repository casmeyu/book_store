from fastapi import FastAPI, HTTPException, status
from sqlalchemy import select, insert, exists
from database.database import DB
from sqlalchemy.orm import joinedload
from config.config import Config
from models.Venta import Venta, Product, venta_product
from schema.product_schema import ProductSchema, Newproduct
from models.user_model import User
from schema.user_schema import NewUser, PublicUserInfo
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
        db.CloseSession()
        return(result)
    
    @app.get("/products/{product_id}", response_model=ProductSchema)
    async def get_product_by_id(product_id):
        config = Config()
        db = DB(config.DbConfig)
        product = db.session.query(Product).get(product_id)
        db.CloseSession()
        return product

    @app.get("/books")
    async def getAllBooks():
        config = Config()
        db = DB(config.DbConfig)
        result = db.session.query(Book).all()
        db.CloseSession()
        return(result)

    @app.post("/products", response_model=ProductSchema)
    async def create_product(prod : Newproduct):
        #Create a new product and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        newproduct = Product(prod.name, prod.price)
        #define identifier to avoid duplicated entries
        #db_productname = db.session.query(Product).filter_by(name = prod.name).first()
        #if db_productname:
        #    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="product already exists on db")
        db.session.add(newproduct)
        db.session.commit()
        db.session.refresh(newproduct)
        db.CloseSession()
        product_info = ProductSchema.model_validate(newproduct)
        return (product_info)

    @app.get("/users/{user_id}", response_model=PublicUserInfo)
    async def get_user_by_id(user_id):
        config = Config()
        db = DB(config.DbConfig)
        user = db.session.query(User).get(user_id)
        db.CloseSession()
        public_user = PublicUserInfo.model_validate(user)
        return public_user

    @app.get("/users", response_model=list[PublicUserInfo])
    async def get_all_users():
        config = Config()
        db = DB(config.DbConfig)
        allUsers = db.session.query(User).all()
        publicUsers = [PublicUserInfo.model_validate(u) for u in allUsers]
        return(publicUsers)

    @app.post("/users", response_model=PublicUserInfo)
    async def create_user(user : NewUser):
        config = Config()
        db = DB(config.DbConfig)

        #Check roles existance
        db_roles = db.session.query(Rol).filter(Rol.id.in_(user.roles)).all()
        if len(db_roles) != len(user.roles):
            #HANDLE ERRORS HANDLE ERRORS
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Roles problem")
        
        # Check user existance
        if (db.session.query(exists().where(User.username == user.username))):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists on database")
        #ver documentacion pydantic response model error

        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        new_user.roles = db_roles
        
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        db.CloseSession()
        
        user_info = PublicUserInfo.model_validate(new_user)
        return(user_info)

    # # Ventas
    @app.get("/ventas")
    async def getAllVentas():
        #RESPONSE MODEL RIGTH NOW!!!
        config = Config()
        db = DB(config.DbConfig)
        ventas = db.session.query(Venta).options(joinedload(Venta.products)).all()
        db.CloseSession()
        return ventas

    @app.post("/ventas", response_model=NewVentaRequest)
    async def createVenta(ventaInfo: NewVentaRequest):
        config = Config()
        db = DB(config.DbConfig)
        
        # Check product existance in DB
        product_ids = [p.id for p in ventaInfo.products]
        db_products = db.session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="one or many products do not exist on database")
            # check specific product error
        
        # Check user in the DB
        if (not db.session.query(exists().where(User.id == ventaInfo.user_id))):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user do not exist on database")
        
        # Calculating final price and getting the products into product_list
        product_list = []
        venta_price = 0.0

        # THIS SHOULD BE CHANGED TO A HASH TABLE INSTEAD OF NESTED FOR LOOPS
        # ALSO THERE IS POSIBBLE ERROR IF I SEND THE SAME ITEM TWICE IN THE VENTA REQUEST
        # This error will be fixed with the hash table but it is a minor thing as of now
        for p in ventaInfo.products:
            item = {
                "quantity": p.quantity
            }
            for db_p in db_products:
                if (p.id == db_p.id):
                    item["product"] = db_p
                    product_list.append(item)
                    venta_price += p.quantity * db_p.price

        new_venta = Venta(ventaInfo.user_id, venta_price)
        db.session.add(new_venta)
        db.session.flush()
        db.session.refresh(new_venta)
        # Add the venta_product relationshinp
        #Here we have another loop
        for item in product_list:
            db.session.execute(venta_product.insert().values(
                venta_id=new_venta.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
                )
            )
        db.session.commit()      
        new_venta = db.session.query(Venta).options(joinedload(Venta.products)).where(Venta.id == new_venta.id)
        db.CloseSession()
        # TRANSFORM VENTA TO PYDANTIC SCHEMA!!!
        return(ventaInfo)
        
    
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
        #add error handling
    
    @app.post("/books", response_model=Book_pydantic)
    async def create_book(book : Book_pydantic):
        #Create a new book and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        newbook = Book(book.isbn, book.title, book.author, book.publisher, book.price)
        db.session.add(newbook)
        db.session.commit()
        db.CloseSession()
        return(book)

def createServer():
    config = Config()
    app = FastAPI()
    setupServerRoutes(app)
    db = DB(config.DbConfig)
    db.MakeMigration()
    return app

