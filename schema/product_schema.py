from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt

class ProductSchema(BaseModel):
    id : int 
    name : str
    price : PositiveFloat
    quantity : PositiveInt

    class Config:
        from_attributes=True
        
class NewProduct(BaseModel):
    name : str
    price : PositiveFloat
    quantity : PositiveInt
    
    class Config:
        from_attributes=True

        
class UpdateStock(BaseModel):
    quantity : int