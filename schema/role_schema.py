from pydantic import BaseModel
from typing import Optional

class RoleSchema(BaseModel):
    id : Optional[int]
    name : str