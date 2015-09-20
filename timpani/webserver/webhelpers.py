import flask
from .. import auth
import urllib.parse

def checkForSession():
	if "uid" in flask.session:
		session = auth.validateSession(flask.session["uid"])
		if session != None:
			return session
	return None

def redirectAndSave(path):	
	flask.session["donePage"] = urllib.parse.urlparse(flask.request.url).path
	return response

def recoverFromRedirect():
	donePage = flask.request.cookies["donePage"]
	response = flask.make_response(flask.redirect(donePage))	
	response.set_cookie("donePage", "", expires=0)
	return response

def canRecoverFromRedirect():
	if "donePage" in flask.session:
		return flask.session["donePage"]
	return None

