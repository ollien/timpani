import os
import os.path
import binascii
import json
from . import database
from . import configmanager
from . import webserver

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs")) 

def run(host = "0.0.0.0", port = 8080, startServer = True):
	#Setup Config manager
	configs = configmanager.ConfigManager(CONFIG_PATH)
	databaseConfig = configs["database"]
	authConfig = configs["auth"]
	if authConfig["signing_key"] == "my_secret_key":
		authConfig["signing_key"] = binascii.hexlify(os.urandom(1024)).decode("utf-8")
		f = open(os.path.join(CONFIG_PATH, "auth.json"), "w")
		f.write(json.dumps(authConfig))
		f.close()
		configs.getConfigs()

	print("[Timpani] Configs loaded.")

	#Register a connection to our database
	databaseConnection = database.DatabaseConnection(connectionString = databaseConfig["connection_string"])
	database.ConnectionManager.addConnection(databaseConnection, "main")
	print("[Timpani] Database sessions started.")

	if startServer:
		webserver.start(host = host, port = port)
	else:
		return webserver.app
