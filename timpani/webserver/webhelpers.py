import flask
import functools
import urllib.parse
from .. import auth
from .. import themes
from .. import database
from .. import settings

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

#Decorator which checks if a user logged in and capable of using the specified permissions. 
#If redirectPage is equal to none,
#the target funciton MUST have the arguments authed and authMessage defined.
def checkUserPermissions(redirectPage = None, saveRedirect = True, redirectMessage = INVALID_PERMISSIONS_FLASH_MESSAGE, requiredPermissions = None):
	def decorator(function):
		def decorated(*args, **kwargs):
			session = checkForSession()	
			if session != None:
				username = session.user.username
				result = True
				#If we don't have any permissions necessary, a login is enough. 
				#Otherwise, we're going to check to make sure that all necessary permissions are in place.
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
		#We don't want to save the redirect if either the user page doesn't need it or there's one already saved
		if canRecoverFromRedirect() or not saveRedirect:
			return flask.redirect(redirectPage)
		else:
			return redirectAndSave(redirectPage)
	else:
		return function(authed = False, authMessage = redirectMessage, *args, **kwargs)

#Decorator to accomodate for SQLAlchamey session life.
#Creates a session on request, closes it after.
def usesDatabase(connectionName):
	def decorator(function):
		def decorated():
			databaseConnection = database.ConnectionManager.getConnection("main")
			databaseConnection.createSession()
			result = function()
			databaseConnection.closeSession()
			return result
		return decorated
	return decorator
		
#Will return all information that is needed to render a post.
#Prevents fragmentation in various post display methods
def getPostsParameters():
	title = settings.getSettingValue("title")
	subtitle = settings.getSettingValue("subtitle")
	displayName = settings.getSettingValue("display_name")
	theme = themes.getCurrentTheme()
	return {
		"blogTitle": title,
		"blogSubtitle": subtitle,
		"displayName": displayName,
		"theme": theme["theme"]
	}	

#Renders the theme's template if the theme contains one
#Otherwise, it renders the default template
def renderPosts(defaultPath, *args, **kwargs):
	theme = themes.getCurrentTheme()
	template = theme["template"]
	if template == None:
		templateFile = open(defaultPath, "r")
		template = templateFile.read()
		templateFile.close()
	return flask.render_template_string(template, *args, **kwargs)
