from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy import Table, Column, Integer, Float, Sequence, ForeignKey, DateTime
from Product import Product
import datetime

Base = declarative_base()

venta_product = Table(
    "venta_product",
    Base.metadata,
    Column("venta_id", ForeignKey("ventas.id"), primary_key=True),
    Column("product_id", ForeignKey("product.id"), primary_key=True),
    Column("quantity", Integer),
    Column("price", Float)
)
class VentaProduct:
    def __init__(self, product:Product, quantity:int):
        self.product:Product = product
        self.quantity:int = quantity

class Venta(Base):
    __tablename__ = "ventas"

    id:int = Column(Integer, Sequence("venta_id_seq"), primary_key=True, nullable=False)
    user_id:int = ForeignKey(("products.id"))
    date:datetime = Column("date", DateTime),
    price:float = Column(Integer, nullable=False)
    products:list[Product] = relationship(secondary="venta_product")

    def __init__(self, user_id:int, products:list[VentaProduct]):
        finalPrice:float = 0.0
        self.user_id = user_id
        self.date = datetime.date.now()
        for item in products:
            self.products.append(item.product)
            finalPrice += (item.product.price * item.quantity)
        print(f'Created Venta user {self.user_id} - {self.date}\n{self.products}')

    def __repr__(self):
        return f"<Venta(id={self.id}, user_id='{self.user_id}', price='{self.price}')>"
