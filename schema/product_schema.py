from pydantic import BaseModel
from typing import Optional

class ProductSchema(BaseModel):
    id : Optional[int] # NO ES OPCIONAL?
    name : str
    price : int