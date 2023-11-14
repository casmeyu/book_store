from fastapi import FastAPI
from server.server import Server
from config.config import Config

def setupServerRoutes(server:Server, config:Config):
    app = server.app
    
    @app.get("/")
    async def root():
        return {"message": "Book store home page"}

    @app.get("/api/db/tables")
    async def getDbTables():
        config = Config()
        session = OpenSession(config.DbConfig)
        db_tables = GetDatabaseTables(session)
        return db_tables
        
    @app.get("/products")
    async def getAllProducts():
        config = Config()
        print("JOJOJO")
        pass

    @app.post("/products")
    async def createProducts():
        #Create a new product and save it in the database
        config = Config()
        conn = OpenConnection(config.DbConfig)
        name = "papa2"
        price = 152
        newproduct = Product(name, price)
        print(newproduct)
        conn.execute(insert(Product).values(name = name, price = price))
        conn.commit()
        CloseConnection(conn)