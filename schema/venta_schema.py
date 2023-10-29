from pydantic import BaseModel
from typing import Optional
from schema.product_schema import ProductSchema
import datetime

class VentaSchema(BaseModel):
    id : int
    user_id : int
    # date : datetime = None
    price : float
    products : list[ProductSchema]
    class Config:
        from_attributes = True



class FinalProductOrder(BaseModel): 
    product: ProductSchema
    quantity: int


class ProductOrder(BaseModel): # USER REQUEST
    id : int
    quantity : int

class NewVentaRequest(BaseModel):
    user_id : int
    products : list[ProductOrder]