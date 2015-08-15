import cherrypy
import jinja2
import os.path

FILE_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "static"))

DEFAULT_CONFIG = {
	"/static": {
		"tools.staticdir.on": True,
		"tools.staticdir.dir": STATIC_ROOT
	}

}

class WebServer():
	def __init__(self, serverConfig = DEFAULT_CONFIG):
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
	server = WebServer()
	server.run()
