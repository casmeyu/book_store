###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection, text, Engine
from sqlalchemy.orm import sessionmaker
from config.config import DbConfig

class DB():    
    def __init__(self, config:DbConfig):
        self.__config:DbConfig = config # __ means private attribute, only the instance it self can acces it
        self.__connection_string:str = f"mysql+mysqlconnector://{config.usr}:{config.pwd}@{config.host}:{config.port}/{config.name}"
        self.__engine:Engine = create_engine(self.__connection_string, echo=True)
        self.name:str = config.name
        self.host:str = config.host
        self.port:int = config.port
        self.connection:Connection = None
        self.session:Session = None
        
        self.OpenConnection()
        self.CloseConnection()
        self.OpenSession()
        self.CloseSession()
    
    # Opens a connection to the database based on the ENV VARIABLES
    def OpenConnection(self):
        try:
            engine = create_engine(self.__connection_string, echo=True)
            self.connection = engine.connect()
        except Exception as ex:
            print("[DATABASE] (OpenConnection) - An error occurred while connecting to the database", ex)
            return False

    # Closes the connection to the database
    def CloseConnection(self):
        try:
            self.connection.close()
            return True
        except Exception as ex:
            print("[DATABASE] (CloseConnection) - An error occurred while closing database connection", ex)
            return False

    # Opens a session to the database based on the ENV VARIABLES
    def OpenSession(self):
        try:
            Session = sessionmaker(bind=self.__engine)
            self.session = Session()
            return True
        except Exception as ex:
            print("[DATABASE] (OpenSession) - An error occurred while opening session to the database", ex)
            return False

    # Closes a session connected to a database
    def CloseSession(self):
        try:
            self.session.close()
            return True
        except Exception as ex:
            print("[DATABASE] (CloseSession) - An error occurred while closing session database", ex)
            return False
        
    # Returns all the tables found in the database
    def GetDatabaseTables(self):
        try:
            result = []
            db_tables = self.session.execute(text("SHOW TABLES;"))
            for row in db_tables.all():
                result.append(row._data[0])
                
            return result
        except Exception as ex:
            print("[Database] (GetDatabaseTables) - An error occurred while getting all the database table names", ex)
            return None