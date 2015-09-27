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
def checkUserPermissions(redirectPage = None, redirectMessage = INVALID_PERMISSIONS_FLASH_MESSAGE, requiredPermissions = None):
	def decorator(function):
		def decorated(*args, **kwargs):
			session = checkForSession()	
			if session != None:
				username = session.user.username
				result = True
				if requiredPermissions != None:
					if type(requiredPermissions) == str:
						result = auth.userHasPermission(username, requiredPermissions)
					else:
						for permission in requiredPermissions:
							if not auth.userHasPermission(username, permission):
								result = False
				if result:
					if redirectPage != None:
						return function(*args, **kwargs)
					else:
						return function(authed = True, authMessage = redirectMessage, *args, **kwargs)
				else:
					flask.flash(redirectMessage)
					if redirectPage != None:
						return flask.redirect(redirectPage)
					else:
						return function(authed = False, authMessage = redirectMessage, *args, **kwargs)
			else:
				flask.flash(redirectMessage)
				if redirectPage != None:
					return flask.redirect(redirectPage)
				else:
					return function(authed = False, authMessage = redirectMessage, *args, **kwargs)
			
		return functools.update_wrapper(decorated, function)
	return decorator
