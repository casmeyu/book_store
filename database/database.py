###
# This Module has the responsability to Open and Close connections to the database
###
from sqlalchemy import create_engine, Connection, text, Engine, MetaData
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database, drop_database
from config.config import DbConfig
from passlib.context import CryptContext


meta = MetaData()
Base = declarative_base(metadata=meta)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#Hash function
class Hasher:

    @staticmethod
    def get_hash_password(plain_password):
        return pwd_context.hash(plain_password)
    
    @staticmethod
    def verify_password(plain_password, hash_password):
        return pwd_context.verify(plain_password, hash_password)

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
        
        self.CreateDatabase()
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
            SessionClass = sessionmaker(bind=self.__engine)
            self.session = SessionClass()
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
            self.CloseSession()
            return result
        except Exception as ex:
            print("[Database] (GetDatabaseTables) - An error occurred while getting all the database table names", ex)
            return None

    def MakeMigration(self):
        meta.create_all(self.__engine)

    def GetAll(self, model:Base, query_options=None):
        try:
            print("Query all")
            if query_options:
                return self.session.query(model).options(query_options).all()
            else:
                return self.session.query(model).all()
        except Exception as ex:
            print("Error occurred")
            print(ex)
            raise ex

    def GetById(self, model:Base, id:any):
        try:
            return self.session.query(model).get(id)
        except Exception as ex:
            print("Error occurred")
            print(ex)
            raise ex
        
    def Insert(self, object:Base, commit:bool=True):
        try:
            self.session.add(object)
            if commit:
                self.session.commit()
                self.session.refresh(object)
            else:
                self.session.flush()
                self.session.refresh(object)
            return object
        except Exception as ex:
            print("Error occurred")
            print(ex)
            raise ex
    def CreateDatabase(self):
        if not database_exists(self.__engine.url):
            create_database(self.__engine.url)
            self.MakeMigration()

    def DropDatabase(self):
        if database_exists(self.__engine.url):
            drop_database(self.__engine.url)
