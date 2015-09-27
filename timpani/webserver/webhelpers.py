import flask
import functools
import urllib.parse
from .. import auth

INVALID_PERMISSIONS_FLASH_MESSAGE = "Sorry, you don't have permission to view that page."

def checkForSession():
	if "uid" in flask.session:
		session = auth.validateSession(flask.session["uid"])
		if session != None:
			return session
	return None

def redirectAndSave(path):	
	flask.session["donePage"] = urllib.parse.urlparse(flask.request.url).path
	return flask.redirect(path)

def markRedirectAsRecovered():
	if "donePage" in flask.session:
		del flask.session["donePage"]
	else:
		raise KeyError("No redirect to be recovered from.")
		
def canRecoverFromRedirect():
	if "donePage" in flask.session:
		return flask.session["donePage"]
	return None

#Decorator function
def checkUserPermissions(requiredPermissions, redirectPage, redirectMessage = INVALID_PERMISSIONS_FLASH_MESSAGE):
	def decorator(function):
		def decorated():
			if type(requiredPermissions) == str:
				requiredPermissions = [requiredPermissions]
			session = checkForSession()	
			username = session.user.username
			result = True
			for permission in requiredPermissions:
				if not auth.userHasPermission(username, permission):
					result = False
			if result:
				return function()
			else:
				flask.flash(redirectMessage)
				return flask.rediret(redirectPage)
		return functools.update_wrapper(decorated, function)
	return decorator
