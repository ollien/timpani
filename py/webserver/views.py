import flask
import os.path
import database
import auth
import blog
import configmanager
from . import webfunctions

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../templates"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
templateConfig = configs["templates"]

blueprint = flask.Blueprint("blogViews", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/")
def show_posts():
	posts = blog.getPosts()
	getPostAuthor = blog.getAuthorFullname if templateConfig["display_full_name"] else blog.getAuthorUsername
	return flask.render_template("posts.html", posts = posts, getPostAuthor = getPostAuthor)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if webfunctions.checkForSession(flask.request):
			return flask.redirect("/manage")	
		else:
			return flask.render_template("login.html")

	elif flask.request.method == "POST":
		if "username" not in flask.request.form or "password" not in flask.request.form:
			return flask.render_template("login.html", error = "A username and password must be provided.")

		elif auth.validateUser(flask.request.form["username"], flask.request.form["password"]):
			resp = webfunctions.recoverFromRedirect() if webfunctions.canRecoverFromRedirect() else flask.make_response(flask.redirect("/manage"))
			resp.set_cookie("sessionId", auth.createSession(flask.request.form["username"]))
			return resp	

		else:
			flask.render_template("login.html", error = "Invalid username or password.")

@blueprint.route("/manage")
def manage():
	session = webfunctions.checkForSession(flask.request)
	if session != None:
		user = auth.getUserFromSession(session)
		return flask.render_template("manage.html", user = user)
	else:
		return webfunctions.redirectAndSave("/login")
