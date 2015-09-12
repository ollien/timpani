import os.path
from . import database
from . import configmanager
from . import webserver

def run(host = "0.0.0.0", port = 8080):
	#Setup Config manager
	configs = configmanager.ConfigManager(os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs")))
	databaseConfig = configs["database"]
	print("[Timpani] Configs loaded.")

	#Register a connection to our database
	databaseConnection = database.DatabaseConnection(connectionString = databaseConfig["connection_string"])
	database.ConnectionManager.addConnection(databaseConnection, "main")
	print("[Timpani] Database sessions started.")

	#Start Webserver.
	webserver.start(host = host, port = port)

	#This will run after server.run finishes, as in, after the server shuts down.
	print("[Timpani] Closing database sessions")
	database.ConnectionManager.closeConnection("main")
