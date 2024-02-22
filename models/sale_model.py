from sqlalchemy import Table, Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped
from models.product_model import Product
from database.database import Base
from datetime import datetime
from typing import List



sale_product = Table(
    "sale_product",
    Base.metadata,
    Column("sale_id", Integer, ForeignKey("sales.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("quantity", Integer),
    Column("price", Float)
)

class Sale(Base):
    __tablename__ = "sales"

    id:int = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id:int = Column(Integer, ForeignKey(("users.id")), nullable=False)
    date:datetime = Column(DateTime, default=datetime.utcnow(), nullable=False)
    price:float = Column(Float, nullable=False)
    products:Mapped[List[Product]] = relationship(secondary="sale_product")

    def __init__(self, user_id:int, price:float, date:datetime = datetime.utcnow()):
        self.user_id = user_id
        self.price = price
        self.date = date

    def __repr__(self):
            return f"<Sale(id={self.id}, user_id='{self.user_id}', date={self.date}, price='{self.price}, products={[prod for prod in self.products]}')>"
