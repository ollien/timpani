import flask
import os.path
import datetime
import urllib.parse
import configmanager
from . import views

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../static"))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))

app = flask.Flask(__name__, static_folder = STATIC_PATH)
app.register_blueprint(views.blueprint)
app.debug = True
