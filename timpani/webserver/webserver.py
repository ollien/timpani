import flask
import os.path
import datetime
import urllib.parse
from .. import configmanager
from . import controllers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../static"))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))

app = flask.Flask(__name__, static_folder = STATIC_PATH)
app.register_blueprint(controllers.user.blueprint)
app.register_blueprint(controllers.admin.blueprint)
app.debug = True
