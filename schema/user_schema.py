from pydantic import BaseModel
from typing import List, Optional
from models.user_model import Rol
from datetime import datetime


class User_pydantic(BaseModel):
    id : Optional[int]
    username : str
    hashed_password : str
    created_at : datetime
    roles : List[Rol]
    is_active : bool
    class Config:
        from_attributes=True

class NewUser(BaseModel):
    username : str
    password : str
    roles    : list[int]
    class Config:
        from_attributes=True

class PublicUserInfo(BaseModel):
    username : str
    is_active : bool
    class Config:
        from_attributes=True
        
class UserInDb(User_pydantic):
    hashed_password : str