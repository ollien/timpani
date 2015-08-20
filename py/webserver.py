import cherrypy
import jinja2
import os.path
import configmanager
import database

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/"))
FILE_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "static"))

CHERRYPY_CONFIG = {
	"/static": {
		"tools.staticdir.on": True,
		"tools.staticdir.dir": STATIC_ROOT
	}

}

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
databaseConfig = configs["database"]

class WebServer():
	def __init__(self, serverConfig = CHERRYPY_CONFIG):
		self.config = serverConfig	
	
	def run(self):
		application = cherrypy.tree.mount(self, "/", config = self.config)
		cherrypy.engine.start()
		cherrypy.engine.block()
		return application

	@cherrypy.expose
	def index(self):
		return "Hello World"


if __name__ == "__main__":
	databaseConnection = database.DatabaseConnection(connectionString = databaseConfig["connection_string"])
	server = WebServer()
	server.run()
