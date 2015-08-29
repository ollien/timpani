import flask
import os.path
import database
import auth
import blog
import configmanager

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))
TEMPLATE_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../templates"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
templateConfig = configs["templates"]
print(TEMPLATE_PATH)
blueprint = flask.Blueprint("blogViews", __name__, template_folder = TEMPLATE_PATH)

@blueprint.route("/")
def show_posts():
	posts = blog.getPosts()
	getPostAuthor = blog.getAuthorFullname if templateConfig["display_full_name"] else blog.getAuthorUsername
	return flask.render_template("posts.html", posts = posts, getPostAuthor = getPostAuthor)
