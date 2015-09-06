import flask
import os.path
import datetime
import urllib.parse
import configmanager
from . import views
from . import endpoints

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../static"))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))

app = flask.Flask(__name__, static_folder = STATIC_PATH)
app.register_blueprint(views.userviews.blueprint)
app.register_blueprint(views.adminviews.blueprint)
app.register_blueprint(endpoints.adminendpoints.blueprint)
app.register_blueprint(endpoints.userendpoints.blueprint)
app.debug = True
