###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection, MetaData
from config.config import DbConfig

meta = MetaData()

# Opens a connection to the database based on the ENV VARIABLES
def Open(config:DbConfig):
    connection_string = f"mysql+mysqlconnector://{config.usr}:{config.pwd}@{config.host}:{config.port}/{config.name}" 
    engine = create_engine(connection_string, echo=True)

    try:
        connection = engine.connect()
        return connection
    except Exception as ex:
        print("[DATABASE] (Open) - An error occurred while connecting to the database", ex)
        return None

# Closes the connection to the database
def Close(openConn:Connection):
    try:
        openConn.close()
        return True
    except Exception as ex:
        print("[DATABASE] (Open) - An error occurred while connecting to the database", ex)
        return False
