import flask
import os.path
import json
import blog
from .. import webhelpers

blueprint = flask.Blueprint("adminEndpoints", __name__)

#Returns a JSON Object based on whether or not the user is logged in.
@blueprint.route("/delete_post/<int:postId>", methods = ["POST"])
def deletePost(postId):
	session = webhelpers.checkForSession()
	if session != None:
		blog.deletePost(postId)
		return json.dumps({"error": 0})

	else:
		return json.dumps({"error": 1}), 403
