from fastapi import FastAPI
from config.config import Config
from server.server import Server
from database.database import DB

# Database Models
from models.product_model import Product
from models.user_model import User, Rol, user_role
from models.Venta import Venta, venta_product
from models.book_model import Book
# Pydantic schemas
from schema.product_schema import ProductSchema
from schema.user_schema import PublicUserInfo, NewUser
from schema.venta_schema import VentaSchema, NewVentaRequest
from schema.rol_schema import Rol_pydantic
from schema.book_schema import Book_pydantic

def setupServerRoutes(server:Server, config:Config):
    app = server.app

    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

    @app.get("/api/db/tables")
    async def getDbTables():
        db_tables = server.db.GetDatabaseTables()
        return db_tables

    @app.get("/products")
    async def getAllProducts():
        result = server.db.session.query(Product).all()
        server.db.CloseSession()
        return(result)
    
    @app.get("/products/{product_id}", response_model=ProductSchema)
    async def get_product_by_id():
        product = server.db.session.query(Product).get(product_id)
        server.db.CloseSession()
        return product

    @app.get("/books")
    async def getAllBooks():
        result = server.db.session.query(Book).all()
        server.db.CloseSession()
        return(result)

    @app.post("/products", response_model=ProductSchema)
    async def create_product(prod : ProductSchema):
        #Create a new product and save it in the database
        new_product = Product(prod.name, prod.price)
        server.db.session.add(new_product)
        server.db.session.commit()
        server.db.session.refresh(new_product)
        server.db.CloseSession()
        product_info = ProductSchema.model_validate(new_product)
        return (product_info)

    @app.get("/users/{user_id}", response_model=PublicUserInfo)
    async def get_user_by_id(user_id):
        user = server.db.session.query(User).get(user_id)
        server,db.CloseSession()
        public_user_info = PublicUserInfo.from_orm(user)
        return public_user_info

    @app.get("/users", response_model=list[PublicUserInfo])
    async def get_all_users():
        allUsers = server.db.session.query(User).all()
        public_users_info = [PublicUserInfo.from_orm(u) for u in allUsers]
        return(public_users_info)

    @app.post("/users", response_model=PublicUserInfo)
    async def create_user(user : NewUser):
        hash_password = Hasher.get_hash_password(user.password)
        new_user = User(user.username, hash_password, str(datetime.now()), True)
        db_roles = server.db.session.query(Rol).filter(Rol.id.in_(user.roles)).all()
        #ver documentacion pydantic response model error
        #Check roles existance only by length comparation
        if len(db_roles) != len(user.roles):
            #HANDLE ERRORS HANDLE ERRORS
            print("ERROR FATAL FALTAN O SOBRAN ROLES")
            return PublicUserInfo(username="ALGO MAL CON LOS ROLES AMIGO", is_active=False)
            # RAISE HTTP EXCEPTION INSTEAD OF RETURN
            
        new_user.roles = db_roles

        server.db.session.add(new_user)
        server.db.session.flush()
        server.db.session.refresh(new_user)
        server.db.session.commit()
        server.db.CloseSession()

        public_user_info = PublicUserInfo.from_orm(new_user)
        return(public_user_info)

    # # Ventas
    @app.get("/ventas")
    async def getAllVentas():
        ventas = server.db.session.query(Venta).options(joinedload(Venta.products)).all()
        server.db.CloseSession()
        # RETURN PYDANTIC SCHEMA
        return ventas

    @app.post("/ventas", response_model=NewVentaRequest)
    async def createVenta(ventaInfo: NewVentaRequest):
        # Check product existance in DB
        product_ids = [p.id for p in ventaInfo.products]
        db_products = server.db.session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            print("ERROR no estan los products")
            # HANDLE ERRORS HANDLE ERRORS
        
        # Check user in the DB
        if (not server.db.session.query(exists().where(User.id == ventaInfo.user_id))):
            print("User does not exist")
            # HANDLE ERRORS HANDLE ERRORS
        
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
        server.db.session.add(new_venta)
        server.db.session.flush()
        server.db.session.refresh(new_venta)
        
        # Add the venta_product relationshinp
        #Here we have another loop
        for item in product_list:
            print("Adding ", item["product"].name)
            server.db.session.execute(venta_product.insert().values(
                venta_id=new_venta.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
                )
            )
        server.db.session.commit()
        server.db.CloseSession()
        # RETURN PYDANTIC SCHEMA INSTEAD OF RETURN
        return(ventaInfo)
        
    
    @app.post("/roles", response_model=Rol_pydantic)
    async def create_rol(rol: Rol_pydantic):
        #Create a new rol and save it in the database
        if (server.db.session.query(exists().where(Rol.name == rol.name))):
            # RAISEAR EXCEPTION ROL YA EXISTE
            pass
        new_rol = Rol(rol.name)
        server.db.session.add(new_rol)
        server.db.session.commit()
        server.db.CloseSession()
        rol_info = Rol_pydantic.model_validate(new_rol)
        return(rol_info)
    
    @app.post("/books", response_model=Book_pydantic)
    async def create_book(book : Book_pydantic):
        #Create a new book and save it in the database
        new_book = Book(book.isbn, book.title, book.author, book.publisher, book.price)
        server.db.session.add(new_book)
        server.db.session.commit()
        server.db.CloseSession()
        # RETURN PYDANTIC SCHEMA
        return(new_book)