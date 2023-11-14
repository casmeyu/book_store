from pydantic import BaseModel
from typing import Optional, List
from schema.product_schema import ProductSchema
from models.product_model import Product
import datetime

class VentaSchema(BaseModel):
    id : int
    user_id : int
    # date : datetime = None
    price : float
    products : List[ProductSchema]
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