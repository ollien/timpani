import flask
import functools
import urllib.parse
import os
import os.path
from .. import auth
from .. import database

THEME_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../themes"))
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

#Decorator which checks if a user logged in and capable of using the specified permissions. If redirectPage is equalt o none the target funciton MUST have the arguments of authed and authMessage defined.
def checkUserPermissions(redirectPage = None, saveRedirect = True, redirectMessage = INVALID_PERMISSIONS_FLASH_MESSAGE, requiredPermissions = None):
	def decorator(function):
		def decorated(*args, **kwargs):
			session = checkForSession()	
			if session != None:
				username = session.user.username
				result = True
				#If we don't have any permissions necessary, a login is enough. Otherwise, we're going to check to make sure that all necessary permissions are in place.
				if requiredPermissions != None:
					if type(requiredPermissions) == str:
						result = auth.userHasPermission(username, requiredPermissions)
					else:
						for permission in requiredPermissions:
							if not auth.userHasPermission(username, permission):
								result = False
				#If all permissions is valid, redirect as needed.
				if result:
					if redirectPage != None:
						return function(*args, **kwargs)
					else:
						return function(authed = True, authMessage = redirectMessage, *args, **kwargs)
				else:
					#We don't want to flash on thigns like ajax routes, so we use redirectPage != None
					willFlash = redirectPage != None
					return _permissionRedirect(redirectPage, saveRedirect, redirectMessage, willFlash)
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
	
def getCurrentTheme():
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.Setting).filter(database.tables.Setting.name == "theme")
	if query.count() > 0:
		themeName = query.first().value
		themes = os.listdir(THEME_PATH)	
		folderName = None
		try:
			folderName = next(theme for theme in themes if theme.lower() == themeName.lower())
		except StopIteration:
			return None

		themeFile = open(os.path.join(THEME_PATH, folderName, "theme.css"), "r")
		theme = themeFile.read()
		themeFile.close()
		return theme
