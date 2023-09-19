from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Sequence, Float, create_engine


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence("product_id_seq"), primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price='{self.price}')>"
