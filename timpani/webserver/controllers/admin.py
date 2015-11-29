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
from ... import themes
from ... import settings

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))
UPLOAD_LOCATION = os.path.abspath(os.path.join(FILE_LOCATION, "../../../static/uploads"))

blueprint = flask.Blueprint("admin", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/manage")
@webhelpers.checkUserPermissions("/login", saveRedirect = False)
def manage():
	return flask.render_template("manage.html", 
		user = webhelpers.checkForSession().user)

@blueprint.route("/add_post", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage", 
	requiredPermissions = auth.CAN_POST_PERMISSION)
def addPost():
	if flask.request.method == "GET":
		return flask.render_template("add_post.html", 
			user = webhelpers.checkForSession().user)
	elif flask.request.method == "POST":
		postTitle = flask.request.form["post-title"]
		postBody = flask.request.form["post-body"].replace("\t", "&emsp;")
		postBody = flask.request.form["post-body"].replace("    ", "&emsp;")
		postTags = flask.request.form["post-tags"]
		blog.addPost(
			title = postTitle, 
			body = postBody, 
			time_posted = datetime.datetime.now(), 
			author = webhelpers.checkForSession().user, 
			tags = postTags)
		return flask.redirect("/")

@blueprint.route("/manage_posts")
@webhelpers.checkUserPermissions("/manage", 
	requiredPermissions = auth.CAN_POST_PERMISSION)
def managePosts():
	posts = blog.getPosts(tags = False)
	return flask.render_template("manage_posts.html", 
		posts = posts, 
			user = webhelpers.checkForSession().user)

@blueprint.route("/edit_post/<int:postId>", methods = ["GET", "POST"])
@webhelpers.checkUserPermissions("/manage", 
	requiredPermissions = auth.CAN_POST_PERMISSION)
def editPost(postId):
	if flask.request.method == "GET":
		post = blog.getPostById(postId)	
		return flask.render_template("add_post.html", 
			post = post, 
			user = webhelpers.checkForSession().user)
	elif flask.request.method == "POST":
		postTitle = flask.request.form["post-title"]
		postBody = flask.request.form["post-body"].replace("\t", "&emsp;")
		postBody = flask.request.form["post-body"].replace("    ", "&emsp;")
		blog.editPost(postId, postTitle, postBody, postTags)
		return flask.redirect("/")

@blueprint.route("/settings", methods = ["GET", "POST"])
@webhelpers.checkUserPermissions("/manage", 
	requiredPermissions = auth.CAN_CHANGE_SETTINGS_PERMISSION)
def settingsPage():
	if flask.request.method == "GET":
		return flask.render_template("settings.html", 
			settings = settings.getAllSettings(),
			themes = themes.getAvailableThemes(),
			user = webhelpers.checkForSession().user)

	if flask.request.method == "POST":
		invalidSettings = []
		for setting in flask.request.form:
			value = flask.request.form[setting]
			valid = True	
			if len(invalidSettings) > 0:
				valid = settings.setSettingValue(setting, value)
			else:
				valid = settings.validateSetting(setting, value)

			if not valid:
				invalidSettings.append(setting)

		if len(invalidSettings) > 0:
			flask.flash("Your settings have been successfully saved.", "success")
			return flask.redirect("/settings")
		else:
			#TODO: Add individual setting validations
			flask.flash("Please be sure all settings are in order.", "error")
			return flask.redirect("/settings"), 400
			

#Returns a JSON Object based on whether or not the user is logged in.
@blueprint.route("/delete_post/<int:postId>", methods = ["POST"])
@webhelpers.checkUserPermissions(requiredPermissions = auth.CAN_POST_PERMISSION)
def deletePost(postId, authed, authMessage):
	if authed:
		blog.deletePost(postId)
		return json.dumps({"error": 0})
	else:
		return json.dumps({"error": 1}), 403

#Returns a JSON Object based on whether or not the user is logged in, 
#or if it's an invalid file type.
@blueprint.route("/upload_image", methods = ["POST"])
@webhelpers.checkUserPermissions(requiredPermissions = auth.CAN_POST_PERMISSION)
def uploadImage(authed, authMessage):
	ACCEPTED_FORMATS = ["image/jpeg", "image/png", "image/gif"]
	if authed:
		image = flask.request.files["image"]
		mime = magic.from_buffer(image.stream.read(), mime = True)
		image.stream.seek(0,0)

		if type(mime) == bytes:
			mime = mime.decode()

		if mime in ACCEPTED_FORMATS:
			extension = mimetypes.guess_extension(mime)
			fileName = "%s%s" % (uuid.uuid4().hex, extension)
			image.save(os.path.join(UPLOAD_LOCATION, fileName))
			return json.dumps({
				"error": 0, 
				"url": os.path.join("/static/uploads", 
				fileName)})
		else:
			return json.dumps({"error": 2}), 400
	else:
		return json.dumps({"error": 1}), 403
