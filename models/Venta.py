from sqlalchemy import Table, Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped
from sqlalchemy.ext.associationproxy import association_proxy
from schema.venta_schema import FinalProductOrder
from models.product_model import Product
from database.database import meta
from datetime import datetime


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
    user_id:int = ForeignKey(("users.id"))
    date:datetime = Column("date", DateTime),
    price:float = Column(Integer, nullable=False)
    products:Mapped[list[Product]] = relationship(secondary="venta_product")

    # product_quantity = association_proxy("venta_product", "quantity") # Adding proxy to access `quantity` in many2many relation table
    # product_price = association_proxy("venta_product", "price") # Adding proxy to access `price` in many2many relation table

    def __init__(self, user_id:int, finalOrder:list[FinalProductOrder]):
        self.price:float = 0.0
        self.user_id = user_id
        self.date = datetime.now()
        print("FINA ORDER?")
        print(finalOrder)
        for item in finalOrder:
            self.products.append(item["product"])
            # self.product_quantity[item["product"]] = item["quantity"]
            # self.product_price[item["product"]] = item["product"].price
            # association_info = self.products.association_proxy(item["product"], 'quantity')
            # association_info = (item["product"].price * item["quantity"])
            print("INSERTING RELATIONSHIP?")

            self.price += (item["product"].price * item["quantity"])

        print(f'Created Venta\nuser {self.user_id} - {self.date}\n{self.products}')

    def __repr__(self):
            return f"<Venta(id={self.id}, user_id='{self.user_id}', date={self.date}, price='{self.price}, products={[prod for prod in self.products]}')>"
