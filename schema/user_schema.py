from pydantic import BaseModel
from typing import List, Optional


class User_pydantic(BaseModel):
    id : Optional[int]
    username : str
    password : str
    created_at : str
    roles : List[int]
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