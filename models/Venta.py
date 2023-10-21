from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy import Table, Column, Integer, Float, ForeignKey, DateTime
from models.product_model import Product
from schema.venta_schema import ProductInVenta
from datetime import datetime
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

    id:int = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id:int = ForeignKey(("users.id"))
    date:datetime = Column("date", DateTime),
    price:float = Column(Integer, nullable=False)
    products:Mapped[list[Product]] = relationship(secondary="venta_product")

    def __init__(self, user_id:int, products:list[ProductInVenta]):
        finalPrice:float = 0.0
        self.user_id = user_id
        self.date = datetime.now()
        for item in products:
            # Chequear product en base de datos con suficiente cantidad
            # Calcular precio total prod.price * item.quantity
            # Guardar relacion venta producto con cantidad y precio final NO GUARDAR EN BASE DE DATOS
            finalPrice += (item.product.price * item.quantity)
        print(f'Created Venta\nuser {self.user_id} - {self.date}\n{self.products}')

    def __repr__(self):
            return f"<Venta(id={self.id}, user_id='{self.user_id}', date={self.date}, price='{self.price}, products={[item.id for item in self.products]}')>"
