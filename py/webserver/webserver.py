import flask
import os.path
import datetime
import urllib.parse
import configmanager
from . import views
FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.abspath(os.path.join(FILE_LOCATION, "../../static"))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))

#configs = configmanager.ConfigManager(os.path.abspath(os.path.join(FILE_LOCATION, "configs")))
#templateConfig = configs["templates"]

app = flask.Flask(__name__, static_folder = STATIC_ROOT)	
app.register_blueprint(views.blueprint)
app.debug = True
