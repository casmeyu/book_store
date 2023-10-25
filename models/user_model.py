from sqlalchemy import Column, Table, Integer, String, Boolean
from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


user_role = Table(
    "user_role",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(200), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    created_at = Column(String(40))
    is_active = Column(Boolean, default=True)
    roles = relationship("Rol", secondary="user_role", back_populates="users")
    

    def __init__(self, username, password, created_at, is_active):
        self.username = username
        self.password = password
        self.created_at = created_at
        self.is_active = is_active

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', password='{self.password}', created_at='{self.created_at}', is_active='{self.is_active}'), roles='{self.roles}'>"

class Rol(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    users = relationship("User", secondary="user_role", back_populates="roles")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Rol(id={self.id}, name='{self.name}')>"
