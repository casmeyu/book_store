import os
from fastapi import HTTPException, status, Depends
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError, jwt
import asyncio
from config.config import Config
from server.server import Server
from database.database import DB, Hasher
# Database Models
from models.user_model import User
# Pydantic schemas
from schema.user_schema import UserSchema
from schema.token_schema import TokenSchema, TokenData

def setupServerRoutes(server:Server, config:Config):
    app = server.db 
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
        #Authenticates the user using the hashed password
        user = get_user(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Missing user")
        if not Hasher.verify_password(password, user.hashed_password):
            # change status code to be more specific
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication problem")
        return user
    
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
    
    
    def get_current_user_role(required_role: str):
        def _get_current_user_role(current_user: User = Depends(get_current_user)):
            if current_user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tienes los permisos necesarios para acceder a esta ruta",
                )
            return current_user
        return _get_current_user_role
    
    
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
    
    #@app.get("/books")
    #async def getAllBooks():
    #    #Gets all books
    #    result = db.GetAll(Book)
    #    return(result)
    #
    #@app.post("/books", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
    #async def create_book(book : BookSchema):
    #    #Create a new book and save it in the database
    #    new_book = Book(book.isbn, book.title, book.author, book.publisher, book.price)
    #    db.Insert(new_book)
    #    db.CloseSession()
    #    return(new_book)