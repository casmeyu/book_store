from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User_pydantic(BaseModel):
    id : Optional[int]
    username : str
    password : str
    is_active : bool

class NewUser(BaseModel):
    username : str
    password : str

class PublicUserInfo(BaseModel):
    username : str
    is_active : bool