###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection, text, MetaData
from sqlalchemy.orm import Session
from config.config import DbConfig

meta = MetaData()

# Opens a connection to the database based on the ENV VARIABLES
def OpenConnection(config:DbConfig):
    try:
        connection_string = f"mysql+mysqlconnector://{config.usr}:{config.pwd}@{config.host}:{config.port}/{config.name}"
        engine = create_engine(connection_string, echo=True)
        connection = engine.connect()
        return connection
    except Exception as ex:
        print("[DATABASE] (OpenConnection) - An error occurred while connecting to the database", ex)
        return None

# Closes the connection to the database
def CloseConnection(openConn:Connection):
    try:
        openConn.close()
        return True
    except Exception as ex:
        print("[DATABASE] (CloseConnection) - An error occurred while closing database connection", ex)
        return False

# Opens a session to the database based on the ENV VARIABLES
def OpenSession(config:DbConfig):
    try:
        connection_string = f"mysql+mysqlconnector://{config.usr}:{config.pwd}@{config.host}:{config.port}/{config.name}"
        engine = create_engine(connection_string, echo=True)
        session = Session(engine)
        return session
    except Exception as ex:
        print("[DATABASE] (OpenSession) - An error occurred while opening session to the database", ex)

# Closes a session connected to a database
def CloseSession(openSession:Session):
    try:
        openSession.close()
        return True
    except Exception as ex:
        print("[DATABASE] (CloseSession) - An error occurred while closing session database", ex)
        return False
    
# Returns all the tables found in the database
def GetDatabaseTables(openSession:Session):
    try:
        result = []
        db_tables = openSession.execute(text("SHOW TABLES;"))
        for row in db_tables.all():
            result.append(row._data[0])
            
        return result
    except Exception as ex:
        print("[Database] (GetDatabaseTables) - An error occurred while getting all the database table names", ex)
        return None