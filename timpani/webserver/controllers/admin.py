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
			if not settings.validateSetting(setting, value):
				invalidSettings.append(setting)

		if len(invalidSettings) == 0:
			for setting in flask.request.form:
				value = flask.request.form[setting]
				settings.setSettingValue(setting, value)

			flask.flash("Your settings have been successfully saved.", "success")
			return flask.redirect("/settings")
		else:
			flask.flash("Invalid settings. Please make sure the following requirements are met and try again.", "error")
			for setting in invalidSettings:
				flask.flash(settings.VALIDATION_MESAGES[setting], "error")
			storedSettings = settings.getAllSettings()
			#Since flask.request.form is an ImmutableMultiDict, we must call to_dict
			#flat = True means we will only get the first value in the dict (which should be fine).
			storedSettings.update(flask.request.form.to_dict(flat = True))
			return flask.render_template("settings.html", 
				settings = storedSettings,
				themes = themes.getAvailableThemes(),
				user = webhelpers.checkForSession().user)

@blueprint.route("/manage_users", methods = ["GET", "POST"])
@webhelpers.checkUserPermissions("/manage",
	requiredPermissions = auth.CAN_CHANGE_SETTINGS_PERMISSION)
def manageUsers():
	if flask.request.method == "GET":
		return flask.render_template("manage_users.html",
			userList = auth.getAllUsers(),
			user = webhelpers.checkForSession().user)

#Returns a JSON Object based on whether or not 
@blueprint.route("/create_user", methods = ["POST"])
@webhelpers.checkUserPermissions(requiredPermissions = auth.CAN_CHANGE_SETTINGS_PERMISSION)
def createUser(authed, authMessage):
	if authed:
		username = flask.request.form["username"]	
		password = flask.request.form["password"]
		fullName = flask.request.form["full_name"]
		canChangeSettings = False
		canWritePosts = False
		if ("can_change_settings" in flask.request.form 
			and flask.request.form["can_change_settings"][1] == "on"):
			canChangeSettings = True
		if ("can_write_posts" in flask.request.form
			and flask.request.form["can_write_posts"][1] == "on"):
			canWritePosts = True
		try:
			auth.createUser(username, fullName, password, canChangeSettings, canWritePosts)
		except ValueError:
			return json.dumps({"error": 2}), 400
		return json.dumps({"error": 0})
	else:
		return json.dumps({"error": 1}), 403

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
