from fastapi import APIRouter, HTTPException, status
from schema.product_schema import ProductSchema, NewProduct, addStock
from models.product_model import Product
from database.database import DB

def setupProductRoutes(db : DB):

    product_router = APIRouter(prefix= "/products")


    @product_router.get("")
    async def getAllProducts():
        #Gets all products from db
        result = db.GetAll(Product)
        return(result)
    
    @product_router.get("/{product_id}", response_model=ProductSchema)
    async def get_product_by_id(product_id:int):
        #Gets a product by its id
        product = db.GetById(Product, product_id)
        db.CloseSession()
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product doesn`t exists")
        return product

    @product_router.post("", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
    async def create_product(prod : NewProduct):
        #Create a new product and save it in the database
        
        #nombre unico??????????????????????????????????????
        new_product = Product(prod.name, prod.price, prod.quantity)
        db.Insert(new_product)
        db.CloseSession()
        return (new_product)
    
    @product_router.patch("/{product_id}/stock", response_model=ProductSchema, status_code=status.HTTP_200_OK)
    async def update_stock(stock_update:addStock, product_id:int):
        #Update product quantity
        if stock_update.quantity <= 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="quantity must be positive")
        db_prod = db.session.query(Product).where(product_id == Product.id).first()
        if not db_prod:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found on db")
        db_prod.quantity += stock_update.quantity
        db.Insert(db_prod)
        db.CloseSession()
        return (db_prod)
    
    return(product_router)