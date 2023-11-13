from sqlalchemy import Column, Integer, String, Float 
from database.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    isbn = Column(String(50), nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    publisher = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)

    def __init__(self, isbn, title, author, publisher, price):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publisher = publisher
        self.price = price

    def __repr__(self):
        return f"<Product(id={self.id}, isbn='{self.isbn}', title='{self.isbn}', author='{self.author}', publisher='{self.publisher}', price='{self.price}')>"
