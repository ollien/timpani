import flask
from .. import auth
import urllib.parse

def checkForSession():
	if "sessionId" in flask.request.cookies:
		session = auth.validateSession(flask.request.cookies["sessionId"])
		if session != None:
			return session
	return None

def redirectAndSave(path):	
	response = flask.make_response(flask.redirect(path))
	print(urllib.parse.urlparse(flask.request.url).path)
	response.set_cookie("donePage", urllib.parse.urlparse(flask.request.url).path)
	return response

def recoverFromRedirect():
	donePage = flask.request.cookies["donePage"]
	response = flask.make_response(flask.redirect(donePage))	
	response.set_cookie("donePage", "", expires=0)
	return response

def canRecoverFromRedirect():
	return "donePage" in flask.request.cookies and flask.request.cookies["donePage"] != ""

