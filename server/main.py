import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

load_dotenv()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_PORT= os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Book store home page"}


@app.get("/users")
async def getAllUsers():
    #Returns all users from the database
    pass

@app.post("/users")
async def createUser():
    #Create a new user and save it in the database
    pass

print("Running uvicorn")
uvicorn.run(app, host="0.0.0.0", port=3001)
print("rainbow")