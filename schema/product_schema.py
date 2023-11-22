from pydantic import BaseModel, NonNegativeInt
from typing import Optional

class ProductSchema(BaseModel):
    id : int 
    name : str
    price : float
    quantity : int

    class Config:
        from_attributes=True
        
class NewProduct(BaseModel):
    name : str
    price : float
    
    class Config:
        from_attributes=True

        
class UpdateStock(BaseModel):
    quantity : int