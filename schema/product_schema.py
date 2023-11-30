from pydantic import BaseModel
from pydantic.types import PositiveFloat, PositiveInt, NonNegativeInt

class ProductSchema(BaseModel):
    id : int 
    name : str
    price : PositiveFloat
    quantity : NonNegativeInt

    class Config:
        from_attributes=True
        
class NewProduct(BaseModel):
    name : str
    price : PositiveFloat
    quantity : PositiveInt
    
    class Config:
        from_attributes=True

        
class addStock(BaseModel):
    quantity : PositiveInt