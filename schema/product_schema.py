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
    quantity : int
    
    class Config:
        from_attributes=True
    
class UpdateProductStock(BaseModel):
    name : str
    quantity : int
    
    class Config:
        from_attributes=True