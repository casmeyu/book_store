from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Sequence
from datetime import datetime

Base = declarative_base()


class User_model(Base):
    __tablename__ = "products"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(datetime.now, nullable=False)
    updated_at = Column(datetime.now, nullable=False)
    deleted_at = Column(datetime.now, nullable=True)
    

    def __init__(self, name, username, password, created_at, updated_at, deleted_at):
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def __repr__(self):
        return f"<Product(id={self.id}, username='{self.username}', password='{self.password}', created_at='{self.created_at}', updated_at='{self.updated_at}', deleted_at='{self.deleted_atted_at}')>"

class pydantic_user(BaseModel):
    name = str