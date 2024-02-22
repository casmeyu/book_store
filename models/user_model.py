from sqlalchemy import Column, Table, Integer, String, Boolean, DateTime
from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped
from database.database import Base
from datetime import datetime


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
    hashed_password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    is_active = Column(Boolean, default=True)
    roles = relationship("Role", secondary="user_role", back_populates="users")
    

    def __init__(self, username, hashed_password, created_at, is_active):
        self.username = username
        self.hashed_password = hashed_password
        self.is_active = is_active

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', hashed_password='{self.hashed_password}', created_at='{self.created_at}', is_active='{self.is_active}'), roles='{self.roles}'>"

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(200), nullable=False)
    users:Mapped[User] = relationship("User", secondary="user_role", back_populates="roles")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"
