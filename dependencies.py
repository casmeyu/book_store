import os
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.database import DB
from models.user_model import User
from schema.token_schema import TokenSchema, TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def common_parameters(token: str):
    raise HTTPException(detail="no existe user", status_code=404)
    return {False}

def get_token_data(token: str = Depends(oauth2_scheme)):
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


def get_user(username: str):
       #gets a certain user from db if it exists
       userindb = db.GetUserByUsername(User, username)
       if not userindb:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found on db")
       return userindb
