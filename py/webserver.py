import cherrypy
import os.path
import database
import templates

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/"))
FILE_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "static"))

CHERRYPY_CONFIG = {
	"/static": {
		"tools.staticdir.on": True,
		"tools.staticdir.dir": STATIC_ROOT
	}

}

class WebServer():
	def __init__(self, serverConfig = CHERRYPY_CONFIG):
		self.config = serverConfig	
		self.templates = templates.TemplateManager()
	
	def run(self):
		application = cherrypy.tree.mount(self, "/", config = self.config)
		cherrypy.engine.start()
		cherrypy.engine.block()
		return application

	@cherrypy.expose
	def index(self):
		databaseConnection = database.ConnectionManager.getConnection("main")
		posts = databaseConnection.session.query(database.tables.Post).all()
		#Posts must go newest first.
		posts.reverse()
		return self.templates["posts"].render(posts = posts)


if __name__ == "__main__":
	server = WebServer()
	server.run()
