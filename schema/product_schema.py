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
    quantity : int
    
    class Config:
        from_attributes=True

class UpdateProductStock(BaseModel):
    id : Optional[int] = None
    name : Optional[str] = None
    price : Optional[float] = None
    quantity : Optional[int] = None
    
    class Config:
        from_attributes=True    
class UpdatedStock(BaseModel):
    id : int
    quantity : int
    
    class Config:
        from_attributes=True