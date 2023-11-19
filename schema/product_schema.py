from pydantic import BaseModel

class ProductSchema(BaseModel):
    id : int 
    name : str
    price : float

    class Config:
        from_attributes=True
        
class NewProduct(BaseModel):
    name : str
    price : float
    
    class Config:
        from_attributes=True
    