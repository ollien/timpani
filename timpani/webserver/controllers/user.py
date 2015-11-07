import flask
import os.path
import datetime
from ... import auth
from ... import blog
from ... import configmanager
from ... import settings
from .. import webhelpers

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../templates"))

blueprint = flask.Blueprint("user", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/")
def showPosts():
	posts = blog.getPosts()
	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	return webhelpers.renderPosts(templatePath, 
		posts = posts, **webhelpers.getPostsParameters())

@blueprint.route("/post/<int:postId>")
def showPost(postId):
	post = blog.getPostById(postId)
	if post == None:
		flask.abort(404)
	else:
		templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
		return webhelpers.renderPosts(templatePath, 
			posts = [post], **webhelpers.getPostsParameters())

@blueprint.route("/tag/<tag>")
def showPostsWithTag(tag):
	posts = blog.getPostsWithTag(tag)
	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	return webhelpers.renderPosts(templatePath, 
		posts = posts, **webhelpers.getPostsParameters())

@blueprint.route("/login", methods=["GET", "POST"])
def login():
	if flask.request.method == "GET":
		if webhelpers.checkForSession():
			return flask.redirect("/manage")	
		else:
			return flask.render_template("login.html")

	elif flask.request.method == "POST":
		if ("username" not in flask.request.form 
			or "password" not in flask.request.form):
			flask.flash("A username and password must be provided.")
			return flask.render_template("login.html")
		elif auth.validateUser(flask.request.form["username"], 
								flask.request.form["password"]):
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
