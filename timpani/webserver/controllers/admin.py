import flask
import os.path
import datetime
import json
import uuid
import magic
import mimetypes
from .. import webhelpers
from ... import blog
from ... import auth

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))
UPLOAD_LOCATION = os.path.abspath(os.path.join(FILE_LOCATION, "../../../static/uploads"))

blueprint = flask.Blueprint("admin", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/manage")
def manage():
	session = webhelpers.checkForSession()
	if session != None:
		return flask.render_template("manage.html", user = session.user)
	else:
		return webhelpers.redirectAndSave("/login")

@blueprint.route("/add_post", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage", requiredPermissions = auth.CAN_POST_PERMISSION)
def addPost():
	session = webhelpers.checkForSession()

	if session != None:
		if flask.request.method == "GET":
			return flask.render_template("add_post.html", user = session.user)
		elif flask.request.method == "POST":
			postTitle = flask.request.form["post-title"]
			postBody = flask.request.form["post-body"].replace("\t", "&emsp;").replace("    ", "&emsp;")
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
		return flask.render_template("manage_posts.html", posts = posts, user = session.user)
	else:
		return webhelpers.redirectAndSave("/login")

@blueprint.route("/edit_post/<int:postId>", methods = ["GET", "POST"])
def editPost(postId):
	session = webhelpers.checkForSession()
	if session != None:
		if flask.request.method == "GET":
			post = blog.getPostById(postId)	
			return flask.render_template("add_post.html", post = post, user = session.user)
		elif flask.request.method == "POST":
			postTitle = flask.request.form["post-title"]
			postBody = flask.request.form["post-body"].replace("\t", "&emsp;").replace("    ", "&emsp;")
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

#Returns a JSON Object based on whether or not the user is logged in, or if it's an invalid file type.
@blueprint.route("/upload_image", methods = ["POST"])
def uploadImage():
	ACCEPTED_FORMATS = ["image/jpeg", "image/png", "image/gif"]
	session = webhelpers.checkForSession()

	if session != None:
		image = flask.request.files["image"]
		mime = magic.from_buffer(image.stream.read(), mime = True)
		image.stream.seek(0,0)

		if type(mime) == bytes:
			mime = mime.decode()

		if mime in ACCEPTED_FORMATS:
			extension = mimetypes.guess_extension(mime)
			print(extension)
			fileName = "%s%s" % (uuid.uuid4().hex, extension)
			image.save(os.path.join(UPLOAD_LOCATION, fileName))
			return json.dumps({"error": 0, "url": os.path.join("/static/uploads", fileName)})
		else:
			return json.dumps({"error": 2}), 400
	else:
		return json.dumps({"error": 1}), 403
