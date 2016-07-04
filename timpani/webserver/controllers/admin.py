import flask
import os.path
import datetime
import json
import uuid
import magic
import mimetypes
from sqlalchemy.exc import IntegrityError
from .. import webhelpers
from ... import blog
from ... import auth
from ... import themes
from ... import settings

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../../templates"))
UPLOAD_LOCATION = os.path.abspath(os.path.join(FILE_LOCATION, "../../../static/uploads"))

blueprint = flask.Blueprint("admin", __name__, template_folder=TEMPLATE_PATH)

@blueprint.route("/manage")
@webhelpers.checkUserPermissions("/login", saveRedirect=False)
def manage():
    return flask.render_template("manage.html",
        user=webhelpers.checkForSession().user)

@blueprint.route("/add_post", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage",
    requiredPermissions=auth.CAN_POST_PERMISSION)
def addPost():
    if flask.request.method == "GET":
        return flask.render_template("add_post.html",
            user=webhelpers.checkForSession().user)
    elif flask.request.method == "POST":
        postTitle = flask.request.form["post-title"]
        postBody = flask.request.form["post-body"].replace("\t", "&emsp;")
        postBody = flask.request.form["post-body"].replace("    ", "&emsp;")
        postTags = flask.request.form["post-tags"]
        blog.addPost(
            title=postTitle,
            body=postBody,
            time_posted=datetime.datetime.now(),
            author=webhelpers.checkForSession().user,
            tags=postTags)
        return flask.redirect("/")

@blueprint.route("/manage_posts")
@webhelpers.checkUserPermissions("/manage",
    requiredPermissions=auth.CAN_POST_PERMISSION)
def managePosts():
    posts = blog.getPosts(tags=False)
    return flask.render_template("manage_posts.html",
        posts=posts,
        user=webhelpers.checkForSession().user)

@blueprint.route("/edit_post/<int:postId>", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage",
    requiredPermissions=auth.CAN_POST_PERMISSION)
def editPost(postId):
    if flask.request.method == "GET":
        post = blog.getPostById(postId)
        return flask.render_template("add_post.html",
            post=post,
            user=webhelpers.checkForSession().user)
    elif flask.request.method == "POST":
        postTitle = flask.request.form["post-title"]
        postBody = flask.request.form["post-body"].replace("\t", "&emsp;")
        postBody = flask.request.form["post-body"].replace("    ", "&emsp;")
        postTags = flask.request.form["post-tags"]
        blog.editPost(postId, postTitle, postBody, postTags)
        return flask.redirect("/")

@blueprint.route("/settings", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage",
    requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION)
def settingsPage():
    if flask.request.method == "GET":
        return flask.render_template("settings.html",
            settings=settings.getAllSettings(),
            themes=themes.getAvailableThemes(),
            user=webhelpers.checkForSession().user)

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
            storedSettings.update(flask.request.form.to_dict(flat=True))
            return flask.render_template("settings.html",
                settings=storedSettings,
                themes=themes.getAvailableThemes(),
                user=webhelpers.checkForSession().user)

@blueprint.route("/manage_users", methods=["GET", "POST"])
@webhelpers.checkUserPermissions("/manage",
    requiredPermissions = auth.CAN_CHANGE_SETTINGS_PERMISSION)
def manageUsers():
    if flask.request.method == "GET":
        return flask.render_template("manage_users.html",
            userList = auth.getAllUsers(),
            user = webhelpers.checkForSession().user)

#Returns a JSON Object based on whether or not user is logged in and if creation was succuessful.
@blueprint.route("/create_user", methods=["POST"])
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION,
    saveRedirect=False)
def createUser(authed, authMessage):
    if authed:
        username = flask.request.form["username"]
        password = flask.request.form["password"]
        fullName = flask.request.form["full_name"]
        canChangeSettings = False
        canWritePosts = False
        if (auth.CAN_POST_PERMISSION in flask.request.form
            and flask.request.form[auth.CAN_POST_PERMISSION] == "on"):
            canChangeSettings = True
        if (auth.CAN_CHANGE_SETTINGS_PERMISSION in flask.request.form
            and flask.request.form[auth.CAN_CHANGE_SETTINGS_PERMISSION] == "on"):
            canWritePosts = True
        user = None
        try:
            user = auth.createUser(username, fullName, password, canChangeSettings, canWritePosts)
        except IntegrityError:
            return json.dumps({"error": 2}), 400
        return json.dumps({"error": 0, "user_id": user.id})
    else:
        return json.dumps({"error": 1}), 403

#Returns a JSON object based on whether or not user is logged in and if a user is found.
#Object contains user information
@blueprint.route("/get_user_info/<int:userId>")
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION)
def getUserInfo(userId, authed, authMessage):
    if authed:
        user = auth.getUserById(userId)
        if user is None:
            return json.dumps({"error": 2})
        userPermissions = []
        if user.can_change_settings:
            userPermissions.append(auth.CAN_CHANGE_SETTINGS_PERMISSION)
        if user.can_write_posts:
            userPermissions.append(auth.CAN_POST_PERMISSION)

        userInfo = {
            "username": user.username,
            "full_name": user.full_name,
            "permissions" : userPermissions
        }
        return json.dumps({"error": 0, "info": userInfo})
    else:
        return json.dumps({"error": 1}), 403

#Returns a JSON Object based on whether or not the user is logged in.
@blueprint.route("/delete_post/<int:postId>", methods=["POST"])
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_POST_PERMISSION,
    saveRedirect=False)
def deletePost(postId, authed, authMessage):
    if authed:
        blog.deletePost(postId)
        return json.dumps({"error": 0})
    else:
        return json.dumps({"error": 1}), 403

#Returns a JSON Object based on whether or not the user is logged in,
#or if it's an invalid file type.
@blueprint.route("/upload_image", methods=["POST"])
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_POST_PERMISSION,
    saveRedirect=False)
def uploadImage(authed, authMessage):
    ACCEPTED_FORMATS = ["image/jpeg", "image/png", "image/gif"]
    if authed:
        image = flask.request.files["image"]
        mime = magic.from_buffer(image.stream.read(), mime=True)
        image.stream.seek(0,0)

        if type(mime) == bytes:
            mime = mime.decode()

        if mime in ACCEPTED_FORMATS:
            extension = mimetypes.guess_extension(mime)
            fileName = "{}{}".format(uuid.uuid4().hex, extension)
            image.save(os.path.join(UPLOAD_LOCATION, fileName))
            return json.dumps({
                "error": 0,
                "url": os.path.join("/static/uploads",
                fileName)})
        else:
            return json.dumps({"error": 2}), 400
    else:
        return json.dumps({"error": 1}), 403

@blueprint.route("/reset_password", methods=["POST"])
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION,
    saveRedirect=False)
def resetPassword(authed, authMessage):
    if authed:
        userId = flask.request.form["userId"]
        newPassword = flask.request.form["password"]
        auth.resetPasswordById(userId, newPassword)
        return json.dumps({"error": 0})
    else:
        return json.dumps({"error": 1}), 403

@blueprint.route("/change_user_permisisons", methods=["POST"])
@webhelpers.checkUserPermissions(requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION,
    saveRedirect=False)
def changePermissions(authed, authMessage):
    if authed:
        if (auth.CAN_POST_PERMISSION in flask.request.form
            and flask.request.form[auth.CAN_POST_PERMISSION] == "on"):
            auth.grantUserPermissionById(flask.request.form["userId"], auth.CAN_POST_PERMISSION)
        else:
            auth.revokeUserPermissionById(flask.request.form["userId"], auth.CAN_POST_PERMISSION)

        if (auth.CAN_CHANGE_SETTINGS_PERMISSION in flask.request.form
            and flask.request.form[auth.CAN_CHANGE_SETTINGS_PERMISSION] == "on"):
            auth.grantUserPermissionById(flask.request.form["userId"], auth.CAN_CHANGE_SETTINGS_PERMISSION)
        else:
            auth.revokeUserPermissionById(flask.request.form["userId"], auth.CAN_CHANGE_SETTINGS_PERMISSION)

        return json.dumps({"error": 0})

    else:
        return json.dumps({"error": 1})

@blueprint.route("/delete_user/<int:user_id>", methods=["POST"])
@webhelpers.checkUserPermission(requiredPermissions=auth.CAN_CHANGE_SETTINGS_PERMISSION,
    saveRedirect=False)
def deleteUser(userId, authed, authMessage):
    if authed:
        auth.deleteUserById(userId)
        return json.dumps({"error": 0})
    else:
        json.dumps({"error": 1})
