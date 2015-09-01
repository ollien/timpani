import flask
import os.path
import json
import datetime
import database
import auth
import blog
import configmanager
from . import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
templateConfig = configs["templates"]

blueprint = flask.Blueprint("blogViews", __name__, template_folder = TEMPLATE_PATH)

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

@blueprint.route("/add_post", methods=["GET", "POST"])
def addPost():
	session = webhelpers.checkForSession()
	if session != None:
		if flask.request.method == "GET":
			return flask.render_template("add_post.html")

		elif flask.request.method == "POST":
			postTitle = flask.request.form["post-title"]
			postBody = flask.request.form["post-body"]
			postTags = flask.request.form["post-tags"]
			blog.addPost(postTitle, postBody, datetime.datetime.now(), session.user, postTags)
			return flask.redirect("/")

		else:
			return webhelpers.redirectAndSave("/login")

@blueprint.route("/manage_posts")
def managePosts():
	session = webhelpers.checkForSession()
	if session != None:
		posts = blog.getPosts(tags = False)
		return flask.render_template("manage_posts.html", posts = posts)

	else:
		return webhelpers.redirectAndSave("/login")

@blueprint.route("/edit_post/<int:postId>", methods = ["GET", "POST"])
def editPost(postId):
	session = webhelpers.checkForSession()
	if session != None:
		if flask.request.method == "GET":
			post = blog.getPostById(postId)	
			return flask.render_template("add_post.html", post = post)
		elif flask.request.method == "POST":
			postTitle = flask.request.form["post-title"]
			postBody = flask.request.form["post-body"]
			postTags = flask.request.form["post-tags"]
			blog.editPost(postId, postTitle, postBody, postTags)
			return flask.redirect("/")
	else:
		webhelpers.redirectAndSave("/login")

#Returns a JSON Object based on whether or not the user is logged in.
@blueprint.route("/delete_post/<int:postId>", methods = ["POST"])
def deletePost(postId):
	session = webhelpers.checkForSession()
	if session != None:
		blog.deletePost(postId)
		return json.dumps({"error": 0})

	else:
		return json.dumps({"error": 1}), 403
