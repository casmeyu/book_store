import os
from dotenv import load_dotenv
load_dotenv()
###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_URL = os.getenv("DB_URL")
DB_PORT=os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

connection_string = f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"


engine = create_engine(connection_string, echo=True)

# Opens a connection to the database based on the ENV VARIABLES
def Open():
    res = {
        "success": False,
        "error": None,
        "result": None
    }
    try:
        connection = engine.connect()
        res.success = True
        res.result = connection
    except Exception as ex:
        print("[DATABASE] (Open) - An error occurred while connecting to the database", ex)
        res.error = ex
    
    return res

# Closes the connection to the database
def Close(openConn:Connection):
    res = {
        "success": False,
        "error": None,
        "result": None
    }
    try:
        openConn.close()
        res.success = True
    except Exception as ex:
        print("[DATABASE] (Open) - An error occurred while connecting to the database", ex)
        res.error = ex
    
    return res
