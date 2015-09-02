import flask
import os.path
import datetime
import blog
from .. import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))

blueprint = flask.Blueprint("adminViews", __name__, template_folder = TEMPLATE_PATH)

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
