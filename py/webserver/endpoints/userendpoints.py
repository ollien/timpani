import flask
import os.path
import json
import uuid
import magic
import mimetypes
import blog
from .. import webhelpers

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
UPLOAD_LOCATION = os.path.abspath(os.path.join(FILE_LOCATION, "../../../static/uploads"))

blueprint = flask.Blueprint("userEndpoints", __name__)
#Returns a JSON Object based on whether or not the user is logged in.
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

