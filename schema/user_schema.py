from pydantic import BaseModel
from typing import List, Optional
from schema.role_schema import RoleSchema
from datetime import datetime


class UserSchema(BaseModel):
    id : Optional[int]
    username : str
    hashed_password : str
    created_at : datetime
    roles : List[RoleSchema]
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
        
class UserInDb(UserSchema):
    hashed_password : str