from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, Float, Connection
from database.database import meta


Base = declarative_base(metadata=meta)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence("product_id_seq"), primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price='{self.price}')>"
