import flask
import os.path
import database
import auth
import blog

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "../templates"))
blueprint = flask.Blueprint("blogViews", __name__, template_folder = TEMPLATE_ROOT)

@blueprint.route("/")
def hello_world():
	return "Hello World"

