from pydantic import BaseModel

class ProductSchema(BaseModel):
    id : int
    name : str
    price : int

    class Config:
        from_attributes=True