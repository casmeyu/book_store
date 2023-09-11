###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection

# Opens a connection to the database based on the ENV VARIABLES
def Open(user:str, pwd:str, uri:str, port:str, db_name:str):
    res = {
        "success": False,
        "error": None,
        "result": None
    }
    connection_string = f"mysql+mysqlconnector://{user}:{pwd}@{uri}:{port}/{db_name}"
    engine = create_engine(connection_string, echo=True)

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
