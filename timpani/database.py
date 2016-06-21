import sqlalchemy
import sqlalchemy.orm
import uuid
import os.path
from . import configmanager
from . import tables

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/"))
configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
config = configs["database"]

class ConnectionManager():
    _connections = {}

    @staticmethod
    def addConnection(connection, connectionName = uuid.uuid4().hex):
        if type(connectionName) == str:
            if type(connection) == DatabaseConnection:
                ConnectionManager._connections[connectionName] = connection
                return connectionName
            elif type(connection) == str:
                c = DatabaseConnection(connection)
                ConnectionManager._connections[connectionName] = connection
                return connectionName
            else:
                raise ValueError("connection must be of type str, not {}".format(type(connection)))
        else:
            raise ValueError("connectionName must be of type str, not {}".format(type(connectionName)))
    
    @staticmethod
    def getConnection(connectionName):
        if type(connectionName) == str:
            try:
                return ConnectionManager._connections[connectionName]
            except KeyError:
                return None

    #Convenience method to get main database connection
    @staticmethod
    def getMainConnection():
        return ConnectionManager.getConnection("main")

    @staticmethod	
    def closeConnection(connectionName):
        if type(connectionName) == str:
            connection = ConnectionManager.getConnection(connectionName)
            if connection != None:
                connection.closeSession()
                del ConnectionManager._connections[connectionName]
            else:
                raise ValueError("connectionName does not exist, or is already closed.")
        else:
            raise ValueError("connectionName must be of type str, not {}".format(type(name)))

class DatabaseConnection():
    def __init__(self, connectionString = config["connection_string"], createTables = True):
        self.connectionString = connectionString
        self.engine = sqlalchemy.create_engine(self.connectionString)
        self._Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
        self.session = self._Session()
        #Create all tables
        if createTables:
            attrs = dir(tables)
            for attr in attrs:
                attr = getattr(tables, attr)
                if isinstance(attr, type) and attr != tables.Base:
                    attr.metadata.create_all(self.engine)	
        
    def getSelectedDatabase(self):
        result = self.session.execute("SELECT DATABASE()").fetchone()
        if result != None:
            return result[0]
        return None
    
    def closeSession(self):
        if self.session != None:
            self.session.close()
    
