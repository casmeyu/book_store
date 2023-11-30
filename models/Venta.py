from sqlalchemy import Table, Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy.ext.associationproxy import association_proxy
from schema.venta_schema import FinalProductOrder
from models.product_model import Product
from database.database import meta
from datetime import datetime
from typing import List


Base = declarative_base(metadata=meta) # Use a single BASE instead of importing meta

venta_product = Table(
    "venta_product",
    Base.metadata,
    Column("venta_id", Integer, ForeignKey("ventas.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer),
    Column("price", Float)
)

class Venta(Base):
    __tablename__ = "ventas"

    id:int = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id:int = Column(Integer, ForeignKey(("users.id")), nullable=False)
    date:datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)
    price:float = Column(Float, nullable=False)
    products:Mapped[List[Product]] = relationship(secondary="venta_product")

    def __init__(self, user_id:int, price:float, date:datetime = datetime.utcnow()):
        self.user_id = user_id
        self.price = price
        self.date = date

    def __repr__(self):
            return f"<Venta(id={self.id}, user_id='{self.user_id}', date={self.date}, price='{self.price}, products={[prod for prod in self.products]}')>"
