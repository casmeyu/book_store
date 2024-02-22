from fastapi import APIRouter, status, HTTPException
from database.database import DB
from schema.sale_schema import NewSaleRequest
from models.product_model import Product
from models.sale_model import sale_product, Sale
from models.user_model import User
from sqlalchemy.orm import joinedload
from sqlalchemy import exists



def setupSaleRoutes(db : DB):

    sale_router = APIRouter(prefix = "/sales")
    
    @sale_router.get("")
    async def getAllSales():
        #Gets all sales on db
        #RESPONSE MODEL RIGTH NOW!!!
        sales = db.GetAll(Sale, joinedload(Sale.products))
        db.CloseSession()
        return sales

    #check sales on db !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    @sale_router.post("", response_model=NewSaleRequest, status_code=status.HTTP_201_CREATED)
    async def createSale(saleInfo: NewSaleRequest):
        #Create a new sale and save it in the database
        # Check product existance in DB
        product_ids = [p.id for p in saleInfo.products]
        db_products = db.session.query(Product).filter(Product.id.in_(product_ids)).all()
        if (len(product_ids) != len(db_products)):
            fail_id = []
            for prod_id in product_ids:
                if prod_id not in [p.id for p in db_products]:
                    fail_id.append(prod_id) 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product problem, the next products do not exist: {fail_id}")
        
        #Check products stock
        fail_quantity = []
        for p in saleInfo.products:
            for db_p in db_products:
                if p.id == db_p.id:
                    if db_p.quantity < p.quantity:
                        fail_quantity.append({"id": db_p.id, "stock": db_p.quantity, "requested" : p.quantity})
                    else:
                        db_p.quantity -= p.quantity
                        db.Insert(db_p, False)
        if fail_quantity:
            db.CloseSession()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Quantity problem, the next products do not have enough stock: {fail_quantity}")
        # Check user in the DB
        if (not db.session.query(exists().where(User.id == saleInfo.user_id))):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user doesn`t exist on database")
        
        # Calculating final price and getting the products into product_list
        product_list = []
        sale_price = 0.0

        # THIS SHOULD BE CHANGED TO A HASH TABLE INSTEAD OF NESTED FOR LOOPS
        # ALSO THERE IS POSIBBLE ERROR IF I SEND THE SAME ITEM TWICE IN THE SALE REQUEST
        # This error will be fixed with the hash table but it is a minor thing as of now
        for p in saleInfo.products:
            item = {
                "quantity": p.quantity
            }
            for db_p in db_products:
                if (p.id == db_p.id):
                    item["product"] = db_p
                    product_list.append(item)
                    sale_price += p.quantity * db_p.price

        new_sale = Sale(saleInfo.user_id, sale_price)
        db.Insert(new_sale, False)
        # Add the sale_product relationshinp
        #Here we have another loop
        for item in product_list:
            db.session.execute(sale_product.insert().values(
                sale_id=new_sale.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
                )
            )
        db.session.commit()      
        new_sale = db.session.query(Sale).options(joinedload(Sale.products)).where(Sale.id == new_sale.id)
        db.CloseSession()
        # TRANSFORM SALE TO PYDANTIC SCHEMA!!!
        return(saleInfo)
    
    return(sale_router)