import sqlalchemy
import sqlalchemy.orm
import uuid
import configmanager
import tables
import os.path

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/"))
print(CONFIG_PATH)
configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
config = configs["database"]

class ConnectionManager():
	_connections = {}

	@staticmethod
	def addConnection(self, connection, connectionName = uuid.uuid4().hex):
		if type(connectionName) == str:
			if type(connection) == DatabaseConnection:
				_connections[connectionName] = connection
				return connectionName
			elif type(connection) == str:
				c = DatabaseConnection(connection)
				_connections[connectionName] = connection
				return connectionName
			else:
				raise ValueError("connection must be of type str, not %s", type(connection))
		else:
			raise ValueError("connectionName must be of type str, not %s", type(name))
	
	@staticmethod
	def getConnection(self, connectionName):
		if type(connectionName) == str:
			try:
				return _connections[connectionName]
			except KeyError:
				return None

	@staticmethod	
	def closeConnection(self, connectionName):
		if type(connectionName) == str:
			_connections[connectionName].session.close()
			_connections.close()
			del _connections[connectionName]
		else:
			raise ValueError("connectionName must be of type str, not %s", type(name))

class DatabaseConnection():
	def __init__(self, connectionString = config["connection_string"], createTables = True):
		self.connectionString = connectionString
		print(self.connectionString)
		self.engine = sqlalchemy.create_engine(self.connectionString)
		self._Session = sqlalchemy.orm.sessionmaker(bind = self.engine)
		self.session = self._Session()
		#Create all tables
		if createTables:
			for table in tables.ALL_TABLES:
				table.metadata.create_all(self.engine)	
		
	def getSelectedDatabase(self):
		result = self.session.execute("SELECT DATABASE()").fetchone()
		if result != None:
			return result[0]
		return None
