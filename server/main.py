from fastapi import FastAPI

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