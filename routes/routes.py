from fastapi import HTTPException, status
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from datetime import datetime

from config.config import Config
from server.server import Server
from database.database import DB, Hasher

# Database Models
from models.product_model import Product
from models.user_model import User, Rol
from models.Venta import Venta, venta_product
from models.book_model import Book
# Pydantic schemas
from schema.product_schema import ProductSchema, NewProduct, UpdateStock
from schema.user_schema import PublicUserInfo, NewUser
from schema.venta_schema import NewVentaRequest
from schema.rol_schema import Rol_pydantic
from schema.book_schema import Book_pydantic

def setupServerRoutes(server:Server, config:Config):
    app = server.app
    db = server.db

    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

    @app.get("/api/db/tables")
    async def getDbTables():
        db_tables = db.GetDatabaseTables()
        return db_tables

    @app.get("/products")
    async def getAllProducts():
        #Gets all products from db
        config = Config()
        db = DB(config.DbConfig)
        result = db.GetAll(Product)
        return(result)
    
    @app.get("/products/{product_id}", response_model=ProductSchema)
    async def get_product_by_id(product_id:int):
        #Gets a product by its id
        config = Config()
        db = DB(config.DbConfig)
        product = db.GetById(Product, product_id)
        db.CloseSession()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn`t exists")
        return product


    @app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
    async def create_product(prod : NewProduct):
        #Create a new product and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        if prod.quantity < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity cant be negative")
        new_product = Product(prod.name, prod.price, prod.quantity)
        print(new_product)
        db.Insert(new_product)
        db.CloseSession()
        return (new_product)
    
    
    @app.patch("/products/{product_id}/stock", response_model=ProductSchema, status_code=status.HTTP_200_OK)
    async def update_stock(stock_update:UpdateStock, product_id:int):
        #Update product quantity
        config = Config()
        db = DB(config.DbConfig)
        if stock_update.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be positive")
        db_prod = db.session.query(Product).where(product_id == Product.id).first()
        if not db_prod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found on db")
        db_prod.quantity += stock_update.quantity
        db.Insert(db_prod)
        db.CloseSession()
        return (db_prod)
        
        
    @app.get("/users/{user_id}", response_model=PublicUserInfo)
    async def get_user_by_id(user_id):
        #Gets a user by its id
        config = Config()
        db = DB(config.DbConfig)
        user = db.GetById(User, user_id)
        db.CloseSession()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn`t exists")
        public_user = PublicUserInfo.model_validate(user)
        return public_user

    @app.get("/users", response_model=list[PublicUserInfo])
    async def get_all_users():
        #Gets all users on db
        config = Config()
        db = DB(config.DbConfig)
        users = db.GetAll(User)
        publicUsers = [PublicUserInfo.model_validate(u) for u in users]
        return(publicUsers)

    @app.post("/users", response_model=PublicUserInfo, status_code=status.HTTP_201_CREATED)
    async def create_user(user : NewUser):
        #Create a new user and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        #Check roles existance
        db_roles = db.session.query(Rol).filter(Rol.id.in_(user.roles)).all()
        if len(db_roles) != len(user.roles):
            fail_id = []
            for rol_id in user.roles:
                if rol_id not in [r.id for r in db_roles]:
                    fail_id.append(rol_id)        
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Roles problem, the next roles do not exist: {fail_id}")
        # Check user existance
        if (db.session.query(User).where(User.username == user.username).first()):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists on database")
        #ver documentacion pydantic response model error

        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        new_user.roles = db_roles
        db.Insert(new_user)
        db.CloseSession()
        publicUser = PublicUserInfo.model_validate(new_user)
        return(publicUser)

    # # Ventas
    @app.get("/ventas")
    async def getAllVentas():
        #Gets all ventas on db
        #RESPONSE MODEL RIGTH NOW!!!
        config = Config()
        db = DB(config.DbConfig)
        ventas = db.GetAll(Venta, joinedload(Venta.products))
        db.CloseSession()
        return ventas

    @app.post("/ventas", response_model=NewVentaRequest, status_code=status.HTTP_201_CREATED)
    async def createVenta(ventaInfo: NewVentaRequest):
        #Create a new venta and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        # Check product existance in DB
        product_ids = [p.id for p in ventaInfo.products]
        db_products = db.session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            fail_id = []
            for prod_id in product_ids:
                if prod_id not in [p.id for p in db_products]:
                    fail_id.append(prod_id) 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product problem, the next products do not exist: {fail_id}")
        
        #check for negative quantity!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        #Check products stock
        fail_quantity = []
        for p in ventaInfo.products:
            for db_p in db_products:
                if p.id == db_p.id:
                    if db_p.quantity < p.quantity:
                        fail_quantity.append({"id": db_p.id, "stock": db_p.quantity, "requested" : p.quantity})
                    else:
                        db_p.quantity -= p.quantity
                        db.Insert(db_p, False)
        if fail_quantity:
            db.CloseSession()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Quantity problem, the next products do not have enough stock: {fail_quantity}")
        # Check user in the DB
        if (not db.session.query(exists().where(User.id == ventaInfo.user_id))):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user doesn`t exist on database")
        
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
        db.Insert(new_venta, False)
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
        
    
    @app.post("/roles", response_model=Rol_pydantic, status_code=status.HTTP_201_CREATED)
    async def create_rol(rol: Rol_pydantic):
        #Create a new rol and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        new_rol = Rol(rol.name)
        db.Insert(new_rol)
        db.CloseSession()
        return(new_rol)
    
    @app.get("/books")
    async def getAllBooks():
        #Gets all books
        config = Config()
        db = DB(config.DbConfig)
        result = db.GetAll(Book)
        return(result)
    
    @app.post("/books", response_model=Book_pydantic, status_code=status.HTTP_201_CREATED)
    async def create_book(book : Book_pydantic):
        #Create a new book and save it in the database
        config = Config()
        db = DB(config.DbConfig)
        new_book = Book(book.isbn, book.title, book.author, book.publisher, book.price)
        db.Insert(new_book)
        db.CloseSession()
        return(new_book)