import flask
import os.path
import json
from ... import blog
import uuid
import magic
import mimetypes
from .. import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
UPLOAD_LOCATION = os.path.abspath(os.path.join(FILE_LOCATION, "../../../static/uploads"))

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

#Returns a JSON Object based on whether or not the user is logged in, or if it's an invalid file type.
@blueprint.route("/upload_image", methods = ["POST"])
def uploadImage():
	ACCEPTED_FORMATS = ["image/jpeg", "image/png", "image/gif"]
	session = webhelpers.checkForSession()

	if session != None:
		image = flask.request.files["image"]
		mime = magic.from_buffer(image.stream.read(), mime = True)
		image.stream.seek(0,0)

		if type(mime) == bytes:
			mime = mime.decode()

		if mime in ACCEPTED_FORMATS:
			extension = mimetypes.guess_extension(mime)
			print(extension)
			fileName = "%s%s" % (uuid.uuid4().hex, extension)
			image.save(os.path.join(UPLOAD_LOCATION, fileName))
			return json.dumps({"error": 0, "url": os.path.join("/static/uploads", fileName)})

		else:
			return json.dumps({"error": 2}), 400

	else:
		return json.dumps({"error": 1}), 403
