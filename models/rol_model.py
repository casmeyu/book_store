from sqlalchemy import Column, Integer, String
from database.database import Base


class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    rol = Column(String(200), nullable=False)

    def __init__(self, rol):
        self.rol = rol

    def __repr__(self):
        return f"<Product(id={self.id}, rol='{self.rol}')>"
