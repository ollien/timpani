import flask
import os.path
import datetime
from ... import auth
from ... import blog
from ... import configmanager
from ... import settings
from ... import themes
from .. import webhelpers

TEMPLATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../templates"))

blueprint = flask.Blueprint("user", __name__, template_folder = TEMPLATE_PATH)

PAGE_LIMIT = 5

@blueprint.route("/")
def showPosts():
	posts = blog.getPosts(limit = PAGE_LIMIT)
	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	postParams = webhelpers.getPostsParameters()
	pageTitle = postParams["blogTitle"]
	pageCount = blog.getPageCount(blog.getPostCount(), PAGE_LIMIT)
	nextPageExists = (blog.nextPageExists(blog.getPostCount(), 
		PAGE_LIMIT, 1))
	return webhelpers.renderPosts(templatePath, pageTitle, 1,
		pageCount, nextPageExists, posts = posts)

@blueprint.route("/page/<int:pageNumber>")
def showPostWithPage(pageNumber):
	if pageNumber < 1:
		flask.abort(400)
	posts = blog.getPosts(limit = PAGE_LIMIT, 
		offset = PAGE_LIMIT * (pageNumber - 1))
	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	postParams = webhelpers.getPostsParameters()
	pageTitle = "%s - page %s" % (postParams["blogTitle"], pageNumber)
	pageCount = blog.getPageCount(blog.getPostCount(), PAGE_LIMIT)
	nextPageExists = (blog.nextPageExists(blog.getPostCount(), 
		PAGE_LIMIT, pageNumber))
	return webhelpers.renderPosts(templatePath, pageTitle, pageNumber,
		pageCount, nextPageExists, posts = posts)

@blueprint.route("/post/<int:postId>")
def showPost(postId):
	post = blog.getPostById(postId)
	if post == None:
		flask.abort(404)
	else:
		templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
		postParams = webhelpers.getPostsParameters()
		pageTitle = "%s - %s" % (postParams["blogTitle"], post["post"].title)
		return webhelpers.renderPosts(templatePath, pageTitle, 1,
			1, False, posts = [post])

@blueprint.route("/tag/<tag>")
def showPostsWithTag(tag):
	posts = blog.getPostsWithTag(tag, limit = PAGE_LIMIT)
	if len(posts) == 0:
		flask.abort(404)

	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	postParams = webhelpers.getPostsParameters()
	pageTitle = "%s - #%s" % (postParams["blogTitle"], tag)
	pageCount = blog.getPageCount(blog.getPostWithTagCount(tag), PAGE_LIMIT)
	nextPageExists = (blog.nextPageExists(blog.getPostWithTagCount(tag),
		PAGE_LIMIT, 1))
	return webhelpers.renderPosts(templatePath, pageTitle, 1,
		pageCount, nextPageExists, posts = posts)

@blueprint.route("/tag/<tag>/page/<int:pageNumber>")
def showPostWithTagAndPage(tag, pageNumber):
	if pageNumber < 1:
		flask.abort(400)
	posts = (blog.getPostsWithTag(tag, limit = PAGE_LIMIT, 
		offset = PAGE_LIMIT * (pageNumber - 1)))
	templatePath = os.path.join(TEMPLATE_PATH, "posts.html")
	postParams = webhelpers.getPostsParameters()
	pageTitle = "%s - #%s" % (postParams["blogTitle"], tag)
	pageCount = blog.getPageCount(blog.getPostWithTagCount(tag), PAGE_LIMIT)
	nextPageExists = blog.nextPageExists(blog.getPostWithTagCount(tag),
		PAGE_LIMIT, pageNumber)
	return webhelpers.renderPosts(templatePath, pageTitle, pageNumber,
		pageCount, nextPageExists, posts = posts)

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

@blueprint.route("/static/theme/<path:filePath>")
def themeStatic(filePath):
	currentTheme = themes.getCurrentTheme()
	if currentTheme["staticPath"] is None:
		return "", 404
	staticPath = currentTheme["staticPath"]
	return flask.send_from_directory(staticPath, filePath)
