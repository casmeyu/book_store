from dotenv import load_dotenv
from datetime import datetime

from models.product_model import Product

from models.user_model import User, Role
from models.sale_model import Sale, sale_product

from database.database import meta, DB, Hasher
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
        "hashed_password": Hasher.get_hash_password("pass"),
        "roles": [
            1,
            2
        ]
    },
    {
        "username": "eric",
        "hashed_password": Hasher.get_hash_password("pass"),
        "roles": [
            1,
        ]
    },
    {
        "username": "laura",
        "hashed_password": Hasher.get_hash_password("pass"),
        "roles": [
            3
        ]
    },
]
products = [
    {
        "name": "zapallo",
        "price": 80.0,
        "quantity": 10
    },
    {
        "name": "papa",
        "price": 40.0,
        "quantity": 20
    },
    {
        "name": "tomate",
        "price": 90.0,
        "quantity": 5
    },
    {
        "name": "zanahoria",
        "price": 30.0,
        "quantity": 15
    }
]

sales = [
    {
        "user_id": 1,
        "products": [
            {
                "id": 1,
                "quantity": 3
            },
            {
                "id": 3,
                "quantity": 1
            },
            {
                "id": 4,
                "quantity": 1
            }
        ]
    },
    {
        "user_id": 2,
        "products": [
            {
                "id": 1,
                "quantity": 1
            },
            {
                "id": 2,
                "quantity": 3
            },
            {
                "id": 4,
                "quantity": 2
            }
        ]
    }
]

def delete_all():
    for table in reversed(meta.sorted_tables):
        print(table)
        db.session.execute(table.delete())
    db.session.commit()

def insert_roles():
    for r in roles:
        role = Role(r["name"])
        db.session.add(role)
        db.session.commit()


def insert_users():
    for u in users:
        user = User(u["username"], u["hashed_password"], datetime.utcnow(), True)
        db_roles = db.session.query(Role).filter(Role.id.in_(u["roles"])).all()
        user.roles = db_roles
        db.session.add(user)
        db.session.commit()

def insert_products():
    for p in products:
        product = Product(p["name"], p["price"], p["quantity"])
        db.session.add(product)
        db.session.commit()

def insert_sales():
    for v in sales:
        product_ids = [p["id"] for p in v["products"]]
        db_products:[Product] = db.session.query(Product).filter(Product.id.in_(product_ids))
        final_price = 0
        product_list = []

        for prod in v["products"]:
            item = {
                "quantity": prod["quantity"]
            }
            for db_p in db_products:
                if prod["id"] == db_p.id:
                    item["product"] = db_p
                    product_list.append(item)
                    final_price += prod["quantity"] * db_p.price


        sale = Sale(v["user_id"], final_price)
        db.session.add(sale)
        db.session.flush()
        db.session.refresh(sale)
        
        for item in product_list:
            print("Adding ", item["product"].name)
            db.session.execute(sale_product.insert().values(
                sale_id=sale.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
                )
            )
        db.session.commit()
        db.CloseSession()

print("Deleting Database")
db.DropDatabase()
print("Creating Database")
db.CreateDatabase()
print("Inserting into database", config.DbConfig.name)
insert_roles()
insert_users()

insert_products()
insert_sales()
