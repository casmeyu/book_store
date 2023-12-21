from pydantic import BaseModel
from typing import Optional

class RolSchema(BaseModel):
    id : Optional[int]
    name : str