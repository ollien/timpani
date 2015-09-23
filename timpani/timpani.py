import os.path
from . import database
from . import configmanager
from . import webserver

def run(host = "0.0.0.0", port = 8080, startServer = True):
	#Setup Config manager
	configs = configmanager.ConfigManager(os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs")))
	databaseConfig = configs["database"]
	print("[Timpani] Configs loaded.")

	#Register a connection to our database
	databaseConnection = database.DatabaseConnection(connectionString = databaseConfig["connection_string"])
	database.ConnectionManager.addConnection(databaseConnection, "main")
	print("[Timpani] Database sessions started.")

	if startServer:
		webserver.start(host = host, port = port)
	else:
		return webserver.app
