import sqlalchemy
import sqlalchemy.orm
import uuid
import sys
import inspect
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
				raise ValueError("connection must be of type str, not %s", type(connection))
		else:
			raise ValueError("connectionName must be of type str, not %s", type(connectionName))
	
	@staticmethod
	def getConnection(connectionName):
		if type(connectionName) == str:
			try:
				return ConnectionManager._connections[connectionName]
			except KeyError:
				return None

	@staticmethod	
	def closeConnection(connectionName):
		if type(connectionName) == str:
			connection = ConnectionManager.getConnection(connectionName)
			if connection != None:
				connection.close()
				del ConnectionManager._connections[connectionName]
			else:
				raise ValueError("connectionName does not exist, or is already closed.")
		else:
			raise ValueError("connectionName must be of type str, not %s", type(name))

class DatabaseConnection():
	def __init__(self, connectionString = config["connection_string"], createTables = True):
		self.connectionString = connectionString
		self.engine = sqlalchemy.create_engine(self.connectionString)
		self._Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
		self.session = self._Session()
		#Create all tables
		if createTables:
			classes = inspect.getmembers(sys.modules[tables.__name__], inspect.isclass)
			for table in classes:
				if table[1] == tables.Base:
					continue
				table[1].metadata.create_all(self.engine)	
		
	def getSelectedDatabase(self):
		result = self.session.execute("SELECT DATABASE()").fetchone()
		if result != None:
			return result[0]
		return None
	
	def close(self):
		self.session.close()
