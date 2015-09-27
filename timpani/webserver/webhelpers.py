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

#Decorated which checks if a user logged in and capable of using the specified permissions. If redirectPage is equalt o none the target funciton MUST have the arguments of authed and authMessage defined.
def checkUserPermissions(redirectPage = None, saveRedirect = True, redirectMessage = INVALID_PERMISSIONS_FLASH_MESSAGE, requiredPermissions = None):
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
					return _permissionRedirect(redirectPage, saveRedirect, redirectMessage, True)	
			else:
				return _permissionRedirect(redirectPage, saveRedirect, redirectMessage, False)	
		return functools.update_wrapper(decorated, function)
	return decorator

def _permissionRedirect(redirectPage, saveRedirect, redirectMessage, flash):
	if flash:
		flask.flash(redirectMessage)
	if redirectPage != None:
		#We don't want to save the redirect if either the user page doesn't need it or there's one already saved, as to prevent overwrites.
		if canRecoverFromRedirect() or not saveRedirect:
			return flask.redirect(redirectPage)
		else:
			return redirectAndSave(redirectPage)
	else:
		return function(authed = False, authMessage = redirectMessage, *args, **kwargs)
	
