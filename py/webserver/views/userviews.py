import flask
import os.path
import auth
import blog
import configmanager
from .. import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
templateConfig = configs["templates"]

blueprint = flask.Blueprint("userViews", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/")
def show_posts():
	posts = blog.getPosts()
	return flask.render_template("posts.html", posts = posts)

@blueprint.route("/post/<int:postId>")
def show_post(postId):
	post = blog.getPostById(postId)
	if post == None:
		flask.abort(404)
	else:
		return flask.render_template("posts.html", posts = [post])

@blueprint.route("/tag/<tag>")
def showPostsWithTag(tag):
	posts = blog.getPostsWithTag(tag)
	return flask.render_template("posts.html", posts = posts)

@blueprint.route("/login", methods=["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if webhelpers.checkForSession():
			return flask.redirect("/manage")	
		else:
			return flask.render_template("login.html")

	elif flask.request.method == "POST":
		if "username" not in flask.request.form or "password" not in flask.request.form:
			return flask.render_template("login.html", error = "A username and password must be provided.")

		elif auth.validateUser(flask.request.form["username"], flask.request.form["password"]):
			resp = webhelpers.recoverFromRedirect() if webhelpers.canRecoverFromRedirect() else flask.make_response(flask.redirect("/manage"))
			resp.set_cookie("sessionId", auth.createSession(flask.request.form["username"]))
			return resp	

		else:
			flask.render_template("login.html", error = "Invalid username or password.")

@blueprint.route("/manage")
def manage():
	session = webhelpers.checkForSession()
	if session != None:
		return flask.render_template("manage.html", user = session.user)
	else:
		return webhelpers.redirectAndSave("/login")


