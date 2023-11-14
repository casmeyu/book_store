from sqlalchemy import Column, Integer, String, Float 
from database.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
