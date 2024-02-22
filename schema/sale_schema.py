from pydantic import BaseModel
from typing import List
from schema.product_schema import ProductSchema
from pydantic.types import PositiveInt, PositiveFloat

class SaleSchema(BaseModel):
    id : int
    user_id : int
    # date : datetime = None
    price : PositiveFloat
    products : List[ProductSchema]
    class Config:
        from_attributes = True


class FinalProductOrder(BaseModel): 
    product: ProductSchema
    quantity: PositiveInt


class ProductOrder(BaseModel): # USER REQUEST
    id : int
    quantity : PositiveInt

class NewSaleRequest(BaseModel):
    user_id : int
    products : list[ProductOrder]