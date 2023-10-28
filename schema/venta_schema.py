from pydantic import BaseModel
from typing import Optional
import datetime

class VentaSchema(BaseModel):
    id : int
    user_id : int
    # date : datetime = None
    price : float
    products : list[int]

class ProductInVenta(BaseModel):
    id : int
    price : float
    quantity : int

class NewVentaSchema(BaseModel):
    user_id : int
    products : list[ProductInVenta]

    

    # id:int = Column(Integer, Sequence("venta_id_seq"), primary_key=True, nullable=False)
    # user_id:int = ForeignKey(("products.id"))
    # date:datetime = Column("date", DateTime),
    # price:float = Column(Integer, nullable=False)
    # products:Mapped[list[Product]] = relationship(secondary="venta_product")