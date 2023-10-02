from pydantic import BaseModel
from datetime import datetime


class pydantic_user(BaseModel):
    user_name : str
    password : str
    created_at : datetime
    updated_at : datetime
    deleted_at : datetime
    