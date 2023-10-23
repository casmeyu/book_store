from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class User_pydantic(BaseModel):
    id : Optional[int]
    username : str
    password : str
    created_at : str
    roles : List[int]
    is_active : bool
    