import sqlalchemy
import sqlalchemy.orm
import uuid
import configmanager

class ConnectionManager():
	_connections = {}

	@staticmethod
	def addConnection(self, connection, connectionName = uuid.uuid4().hex):
		if type(connectionName) == str:
			if type(connection) == DatabaseConnection:
				_connections[connectionName] = connection
				return connectionName
			else if type(connection) == str:
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
	def __init__(self, connectionString):
		self.connectionString = configs['connection_string']
		self.engine = sqlalchemy.create_engine(bind = self.connectionString)
		self._Session = sqlalchemy.orm.create_session(bind = engine)
		self.session = Session()
		
	def getSelectedDatabase(self):
		result = session.execute("SELECT DATABASE()").fetchone()
		if result != None:
			return result[0]
		return None
