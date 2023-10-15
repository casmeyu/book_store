from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy import Table, Column, Integer, Float, Sequence, ForeignKey, DateTime
from models.Product import Product
import datetime
from database.database import meta

Base = declarative_base(metadata=meta) # Use a single BASE instead of importing meta

venta_product = Table(
    "venta_product",
    Base.metadata,
    Column("venta_id", Integer, ForeignKey("ventas.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
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
    products:Mapped[list[Product]] = relationship(secondary="venta_product")

    def __init__(self, user_id:int, products:list[VentaProduct]):
        finalPrice:float = 0.0
        self.user_id = user_id
        self.date = datetime.date.now()
        for item in products:
            self.products.append(item.product)
            finalPrice += (item.product.price * item.quantity)
        print(f'Created Venta\nuser {self.user_id} - {self.date}\n{self.products}')

    def __repr__(self):
        return f"<Venta(id={self.id}, user_id='{self.user_id}', date={self.date}, price='{self.price}, products={[item.id for item in self.products]}')>"
