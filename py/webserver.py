import flask
import os.path
import datetime
import urllib.parse
import database
import templates
import auth
import blog

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../configs/"))
FILE_LOCATION = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
STATIC_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "static"))

class WebServer():
	def __init__(self, serverConfig = CHERRYPY_CONFIG):
		self.config = serverConfig	
		self.templates = templates.TemplateManager()
	
	def run(self):
		application = cherrypy.tree.mount(self, "/", config = self.config)
		cherrypy.server.socket_host = '0.0.0.0'
		cherrypy.engine.start()
		cherrypy.engine.block()
		return application

	def checkForSession(self):
		if "sessionId" in cherrypy.request.cookie:
			session = auth.validateSession(cherrypy.request.cookie["sessionId"].value)
			if session != None:
				return session
		return None

	#Allow the user to be redirected and once this page is done being used (in this case login), is redirected back, for something like a login page
	def redirectToLoginAndSave(self):
		cherrypy.response.cookie["donePage"] = urllib.parse.urlparse(cherrypy.url()).path
		raise cherrypy.HTTPRedirect("/login")
	
	#The sister function to redirectToLoginAndSave, which sends the user back after the action has been completed.
	def recoverFromRedirect(self, redirect = True):
		donePage = cherrypy.request.cookie["donePage"].value
		del cherrypy.request.cookie["donePage"]
		if redirect:
			raise cherrypy.HTTPRedirect(donePage)
		else:
			return donePage

	def canRecoverFromRedirect(self):
		return "donePage" in cherrypy.request.cookie

	@cherrypy.expose
	def index(self):
		databaseConnection = database.ConnectionManager.getConnection("main")
		posts = blog.getPosts()
		#If the config says to display the full name, we will return that instead of the username.
		if templates.templateConfig["display_full_name"]:
			getPostAuthor = lambda id: databaseConnection.session.query(database.tables.User).filter(database.tables.User.id == id).first().full_name
		else:
			getPostAuthor = lambda id: databaseConnection.session.query(database.tables.User).filter(database.tables.User.id == id).first().username

		return self.templates["posts"].render(posts = posts, getPostAuthor = getPostAuthor)

	@cherrypy.expose
	def login(self, username = None, password = None):
		if cherrypy.request.method == "GET":
			if self.checkForSession() != None:
				raise cherrypy.HTTPRedirect("/manage")	
			return self.templates["login"].render()
		elif cherrypy.request.method == "POST":
			if username == None or password == None:
				raise cherrypy.HTTPRedirect("/login")	
			if auth.validateUser(username, password):
				sessionId = auth.createSession(username)
				cherrypy.response.cookie["sessionId"] = sessionId

				if self.canRecoverFromRedirect():
					self.recoverFromRedirect()
				else:
					raise cherrypy.HTTPRedirect("/manage")	
			else:
				return self.templates["login"].render(error = "Invalid username or password")

	@cherrypy.expose
	def manage(self):
		session = self.checkForSession()
		if session != None:
			user = auth.getUserFromSession(session)
			return self.templates["manage"].render(user = user)
		else:
			redirectToLoginAndSave()

	@cherrypy.expose
	def add_post(self, postTitle = None, postBody = None, postTags = None):
		if cherrypy.request.method == "GET":
			session = self.checkForSession()
			if session != None:
				user = auth.getUserFromSession(session)
				return self.templates["add_post"].render()
			else:
				self.redirectToLoginAndSave()
		else:
			session = self.checkForSession()
			if session != None:
				user = auth.getUserFromSession(session)
				databaseConnection = database.ConnectionManager.getConnection("main")
				postObj = database.tables.Post(title = postTitle, body = postBody, time_posted = datetime.datetime.now(), author = user.id)
				blog.addPost(postTitle, postBody, datetime.datetime.now(), user.id, postTags)
				raise cherrypy.HTTPRedirect("/")
			else:
				#TODO: See if there's a nice way to store post content in a scenario like this
				self.redirectToLoginAndSave()

if __name__ == "__main__":
	server = WebServer()
	server.run()
