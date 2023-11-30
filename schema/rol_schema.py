from pydantic import BaseModel
from typing import Optional

class Rol_pydantic(BaseModel):
    id : Optional[int]
    name : str