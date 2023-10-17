from pydantic import BaseModel
from typing import Optional

class Product_pydantic(BaseModel):
    id : Optional[int] # NO ES OPCIONAL?
    name : str
    price : int