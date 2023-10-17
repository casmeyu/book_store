
from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base
from sqlalchemy.orm import declarative_base
from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(200), nullable=False)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    

    def __init__(self, username, password, is_active):
        self.username = username
        self.password = password
        self.is_active = is_active

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', password='{self.password}', is_active='{self.is_active}')>"