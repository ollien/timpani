import os
import os.path
import binascii
import json
import sqlalchemy
from . import database
from . import configmanager
from . import webserver

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs")) 

DEFAULT_SETTINGS = {
	"title": "Timpani",
	"subtitle": "Your blog, run using Timpani.",
	"display_name": "full_name"
}

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

	#Setup all default settings
	settingNames = [item == database.tables.Setting.name for item in DEFAULT_SETTINGS]
	settingsQuery = databaseConnection.session.query(database.tables.Setting.name).filter(sqlalchemy.or_(*settingNames))
	result = settingsQuery.all()
	#Get all settings that are not in the database, and set them.
	neededSettings = [setting for setting in DEFAULT_SETTINGS if (setting, ) not in result] #result has all names in a tuple, so we must query as such.
	for item in neededSettings:
		setting = database.tables.Setting(name = item, value = DEFAULT_SETTINGS[item])
		databaseConnection.session.add(setting)
	
	if len(neededSettings) > 0:
		databaseConnection.session.commit()

	if startServer:
		webserver.start(host = host, port = port)
	else:
		return webserver.app
