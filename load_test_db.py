from dotenv import load_dotenv
from datetime import datetime

from models.product_model import Product

from models.user_model import User, Rol, user_role
from models.Venta import Venta, venta_product

from database.database import Base, DB, Hasher
from config.config import Config

load_dotenv()

config:Config = Config()
db:DB = DB(config.DbConfig)

db.MakeMigration()
roles = [
    {
        "name": "admin"
    },
    {
        "name": "seller"
    },
    {
        "name": "user"
    },
]

users = [
    {
        "username": "casmeyu",
        "password": Hasher.get_hash_password("pass"),
        "roles": [
            1,
            2
        ]
    },
    {
        "username": "eric",
        "password": Hasher.get_hash_password("pass"),
        "roles": [
            1,
        ]
    },
    {
        "username": "laura",
        "password": Hasher.get_hash_password("pass"),
        "roles": [
            3
        ]
    },
]


def insert_roles():
    for r in roles:
        rol = Rol(r["name"])
        db.session.add(rol)
        db.session.commit()


def insert_users():
    for u in users:
        user = User(u["username"], u["password"], datetime.utcnow(), True)
        db_roles = db.session.query(Rol).filter(Rol.id.in_(u["roles"])).all()
        print("DB ROLES", db_roles)
        user.roles = db_roles
        print("WHAT IS THE USER?", user)
        db.session.add(User)
        db.session.commit()

print("Inserting into database", config.DbConfig.name)
# insert_roles()
insert_users()

print("Inserted into database")
