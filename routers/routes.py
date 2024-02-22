import os
from fastapi import HTTPException, status, Depends
from sqlalchemy import exists
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
import asyncio

from config.config import Config
from server.server import Server
from database.database import DB, Hasher
# Database Models
from models.product_model import Product
from models.user_model import User, Role
from models.sale_model import Sale, sale_product
from models.book_model import Book
# Pydantic schemas
from schema.product_schema import ProductSchema, NewProduct, addStock
from schema.user_schema import PublicUserInfo, NewUser, UserSchema
from schema.sale_schema import NewSaleRequest
from schema.role_schema import RoleSchema
from schema.book_schema import BookSchema
from schema.token_schema import TokenSchema, TokenData

def setupServerRoutes(server:Server, config:Config):
    app = server.app
    db = server.db

    ###### authentacation #######
    
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
    def get_user(username: str):
        #gets a certain user from db if it exists
        userindb = db.GetUserByUsername(User, username)
        if not userindb:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found on db")
        return userindb
        
        
    def authenticate_user(username: str, password: str):
        #Authenticates the user using his hashed password
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Missing user")
        if not Hasher.verify_password(password, user.hashed_password):
            # change status code to be more specific
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication problem")
        return user
    
    
    def create_access_token(data: dict, expires_delta: timedelta or None = None):
        #Creates a token
        to_encode = data.copy()
        #Must review this
        if expires_delta:
           expire = datetime.utcnow() + expires_delta
        else: 
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, str(os.environ.get("SERCRET_KEY")), algorithm=str(os.environ.get("ALGORITHM")))
        return encoded_jwt
    
    
    def get_current_user(token: str = Depends(oauth2_scheme)):
        #??
        credential_exeption = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials",
        )
        try:
            payload = jwt.decode(token, str(os.environ.get("SERCRET_KEY")), algorithms=str(os.environ.get("ALGORITHM")))
            username: str = payload.get("sub")
            if username is None:
                raise credential_exeption
            token_data = TokenData(username = username)
        except JWTError:
            raise credential_exeption
        user = get_user(username=token_data.username)
        if user is None: 
            raise credential_exeption
        return user
    
    
    def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
        #Checks if the user is active
        asyncio.wait_for(current_user, 10)
        if current_user.is_active == False:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user
    
    
    @app.post("/token", response_model=TokenSchema)
    async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
        #????
        
        user = authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Incorrect username or password", 
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=int(os.environ.get("EXPIRATION_MINUTES")))     
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    
    
    @app.get("/users/me", response_model=UserSchema)
    #Gets the currently authenticated user
    async def read_users_me(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ):
        print ("tamo en la ruta mono", current_user)
        current_user = UserSchema.model_validate(current_user, from_attributes=True)
        return current_user


    @app.get("/users/me/items/")
    async def read_own_items(
        current_user: Annotated[User, Depends(get_current_active_user)]
    ):
        return [{"item_id": "Foo", "owner": current_user.username}]
    
    ##############--------------################
    
    @app.get("/AutTest")
    async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
        return {"token": token}

    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

    @app.get("/api/db/tables")
    async def getDbTables():
        #gets all db tables
        db_tables = db.GetDatabaseTables()
        return db_tables

    #@app.get("/products")
    #async def getAllProducts():
    #    #Gets all products from db
    #    result = db.GetAll(Product)
    #    return(result)
    #
    #@app.get("/products/{product_id}", response_model=ProductSchema)
    #async def get_product_by_id(product_id:int):
    #    #Gets a product by its id
    #    product = db.GetById(Product, product_id)
    #    db.CloseSession()
    #    if not product:
    #        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn`t exists")
    #    return product
#
    #@app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
    #async def create_product(prod : NewProduct):
    #    #Create a new product and save it in the database
    #    
    #    #nombre unico??????????????????????????????????????
    #    new_product = Product(prod.name, prod.price, prod.quantity)
    #    db.Insert(new_product)
    #    db.CloseSession()
    #    return (new_product)
    
    #@app.patch("/products/{product_id}/stock", response_model=ProductSchema, status_code=status.HTTP_200_OK)
    #async def update_stock(stock_update:addStock, product_id:int):
    #    #Update product quantity
    #    if stock_update.quantity <= 0:
    #        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be positive")
    #    db_prod = db.session.query(Product).where(product_id == Product.id).first()
    #    if not db_prod:
    #        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found on db")
    #    db_prod.quantity += stock_update.quantity
    #    db.Insert(db_prod)
    #    db.CloseSession()
    #    return (db_prod)
          
    #@app.get("/users/{user_id}", response_model=PublicUserInfo)
    #async def get_user_by_id(user_id):
    #    #Gets a user by its id
    #    user = db.GetById(User, user_id)
    #    db.CloseSession()
    #    if not user:
    #        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn`t exists")
    #    public_user = PublicUserInfo.model_validate(user)
    #    return public_user
#
    #@app.get("/users", response_model=list[PublicUserInfo])
    #async def get_all_users():
    #    #Gets all users on db
    #    users = db.GetAll(User)
    #    publicUsers = [PublicUserInfo.model_validate(u) for u in users]
    #    return(publicUsers)
#
    #@app.post("/users", response_model=PublicUserInfo, status_code=status.HTTP_201_CREATED)
    #async def create_user(user : NewUser):
    #    #Create a new user and save it in the database
    #    #Check roles existance
    #    db_roles = db.session.query(Role).filter(Role.id.in_(user.roles)).all()
    #    if len(db_roles) != len(user.roles):
    #        fail_id = []
    #        for role_id in user.roles:
    #            if role_id not in [r.id for r in db_roles]:
    #                fail_id.append(role_id)        
    #        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Roles problem, the next roles do not exist: {fail_id}")
    #    # Check user existance
    #    if (db.session.query(User).where(User.username == user.username).first()):
    #        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="username already exists on database")
    #    #ver documentacion pydantic response model error
#
    #    hash_password = Hasher.get_hash_password(user.password)
    #    new_user = User(user.username, hash_password, str(datetime.now()), True)
    #    new_user.roles = db_roles
    #    db.Insert(new_user)
    #    db.CloseSession()
    #    publicUser = PublicUserInfo.model_validate(new_user)
    #    return(publicUser)

    # # Sales
    #@app.get("/sales")
    #async def getAllSales():
    #    #Gets all sales on db
    #    #RESPONSE MODEL RIGTH NOW!!!
    #    sales = db.GetAll(Sale, joinedload(Sale.products))
    #    db.CloseSession()
    #    return sales
#
    ##check sales on db !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #
    #@app.post("/sales", response_model=NewSaleRequest, status_code=status.HTTP_201_CREATED)
    #async def createSale(saleInfo: NewSaleRequest):
    #    #Create a new sale and save it in the database
    #    # Check product existance in DB
    #    product_ids = [p.id for p in saleInfo.products]
    #    db_products = db.session.query(Product).filter(Product.id.in_(product_ids)).all()
    #    if (len(product_ids) != len(db_products)):
    #        fail_id = []
    #        for prod_id in product_ids:
    #            if prod_id not in [p.id for p in db_products]:
    #                fail_id.append(prod_id) 
    #        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product problem, the next products do not exist: {fail_id}")
    #    
    #    #Check products stock
    #    fail_quantity = []
    #    for p in saleInfo.products:
    #        for db_p in db_products:
    #            if p.id == db_p.id:
    #                if db_p.quantity < p.quantity:
    #                    fail_quantity.append({"id": db_p.id, "stock": db_p.quantity, "requested" : p.quantity})
    #                else:
    #                    db_p.quantity -= p.quantity
    #                    db.Insert(db_p, False)
    #    if fail_quantity:
    #        db.CloseSession()
    #        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Quantity problem, the next products do not have enough stock: {fail_quantity}")
    #    # Check user in the DB
    #    if (not db.session.query(exists().where(User.id == saleInfo.user_id))):
    #        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user doesn`t exist on database")
    #    
    #    # Calculating final price and getting the products into product_list
    #    product_list = []
    #    sale_price = 0.0
#
    #    # THIS SHOULD BE CHANGED TO A HASH TABLE INSTEAD OF NESTED FOR LOOPS
    #    # ALSO THERE IS POSIBBLE ERROR IF I SEND THE SAME ITEM TWICE IN THE SALE REQUEST
    #    # This error will be fixed with the hash table but it is a minor thing as of now
    #    for p in saleInfo.products:
    #        item = {
    #            "quantity": p.quantity
    #        }
    #        for db_p in db_products:
    #            if (p.id == db_p.id):
    #                item["product"] = db_p
    #                product_list.append(item)
    #                sale_price += p.quantity * db_p.price
#
    #    new_sale = Sale(saleInfo.user_id, sale_price)
    #    db.Insert(new_sale, False)
    #    # Add the sale_product relationshinp
    #    #Here we have another loop
    #    for item in product_list:
    #        db.session.execute(sale_product.insert().values(
    #            sale_id=new_sale.id,
    #            product_id=item["product"].id,
    #            quantity=item["quantity"],
    #            price=item["product"].price
    #            )
    #        )
    #    db.session.commit()      
    #    new_sale = db.session.query(Sale).options(joinedload(Sale.products)).where(Sale.id == new_sale.id)
    #    db.CloseSession()
    #    # TRANSFORM SALE TO PYDANTIC SCHEMA!!!
    #    return(saleInfo)
        
    #@app.post("/roles", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
    #async def create_role(role: RoleSchema):
    #    #Create a new role and save it in the database
    #    new_role = Role(role.name)
    #    db.Insert(new_role)
    #    db.CloseSession()
    #    return(new_role)
    
    @app.get("/books")
    async def getAllBooks():
        #Gets all books
        result = db.GetAll(Book)
        return(result)
    
    @app.post("/books", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
    async def create_book(book : BookSchema):
        #Create a new book and save it in the database
        new_book = Book(book.isbn, book.title, book.author, book.publisher, book.price)
        db.Insert(new_book)
        db.CloseSession()
        return(new_book)