from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class User_pydantic(BaseModel):
    id : Optional[int]
    username : str
    password : str
    is_active : bool
    