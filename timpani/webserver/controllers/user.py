import flask
import os.path
import datetime
from ... import auth
from ... import blog
from ... import configmanager
from ... import settings
from .. import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
templateConfig = configs["templates"]

blueprint = flask.Blueprint("user", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/")
def showPosts():
	posts = blog.getPosts()
	title = settings.getSettingValue("title")
	subtitle = settings.getSettingValue("subtitle")
	return flask.render_template("posts.html", posts = posts, blogTitle = title, blogSubtitle = subtitle)

@blueprint.route("/post/<int:postId>")
def showPost(postId):
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
			flask.flash("A username and password must be provided.")
			return flask.render_template("login.html")
		elif auth.validateUser(flask.request.form["username"], flask.request.form["password"]):
			donePage = webhelpers.canRecoverFromRedirect()
			donePage = donePage if donePage is not None else "/manage"
			sessionId, expires = auth.createSession(flask.request.form["username"])
			flask.session["uid"] = sessionId
			flask.session.permanent = True
			flask.session.permanent_session_lifetime = datetime.datetime.now() - expires
			return flask.redirect(donePage)
		else:
			flask.flash("Invalid username or password.")
			return flask.render_template("login.html")

@blueprint.route("/logout", methods=["POST"])
def logout():
	if webhelpers.checkForSession():
		if "uid" in flask.session:
			sessionId = flask.session["uid"]
			auth.invalidateSession(sessionId)
			flask.session.clear()
	
	return flask.redirect("/login")
