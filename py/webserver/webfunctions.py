import flask
import auth
import urllib.parse

def checkForSession(request):
	print(flask.request == request)
	if "sessionId" in request.cookies:
		session = auth.validateSession(request.cookies["sessionId"])
		if session != None:
			return session
	return None
