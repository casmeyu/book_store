from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, Float, Connection
from database.database import meta, Open, Close
from config.config import DbConfig, Config


#product = Table(
#    "products", meta,
#    Column("id", Integer, primary_key=True, nullable=False),
#    Column("name", String(255), nullable=False),
#    Column("price", Integer, nullable=False)
#)
#config = Config()
#meta.create_all(Open(config.DbConfig))

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
