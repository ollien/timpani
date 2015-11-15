import flask
import os.path
import datetime
import urllib.parse
from .. import database
from .. import configmanager
from . import controllers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
STATIC_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../static"))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../../configs/"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
authConfig = configs["auth"]

app = flask.Flask(__name__, static_folder = STATIC_PATH)
app.secret_key = authConfig["signing_key"]
app.register_blueprint(controllers.user.blueprint)
app.register_blueprint(controllers.admin.blueprint)

@app.teardown_request
def teardown_request(exception = None):
	databaseConnection = database.ConnectionManager.getConnection("main")
	databaseConnection.session.close()
