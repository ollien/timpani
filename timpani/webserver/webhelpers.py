import flask
import functools
import bs4
import urllib.parse
from .. import auth
from .. import themes
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

def canRecoverFromRedirect():
    if "donePage" in flask.session:
        return flask.session["donePage"]
    return None

#Decorator which checks if a user logged in and capable of using the specified permissions.
#If redirectPage is equal to none,
#the target funciton MUST have the arguments authed and authMessage defined.
def checkUserPermissions(redirectPage=None, saveRedirect=True, redirectMessage=INVALID_PERMISSIONS_FLASH_MESSAGE, requiredPermissions=None):
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
                        return function(authed=True, authMessage=redirectMessage, *args, **kwargs)
                else:
                    #We don't want to flash on thigns like ajax routes, so we use redirectPage != None
                    willFlash = redirectPage != None
                    return _permissionRedirect(redirectPage, saveRedirect, redirectMessage, willFlash, function, *args, **kwargs)
            else:
                return _permissionRedirect(redirectPage, saveRedirect, redirectMessage, False, function, *args, **kwargs)
        return functools.update_wrapper(decorated, function)
    return decorator

def _permissionRedirect(redirectPage, saveRedirect, redirectMessage, flash, function, *args, **kwargs):
    if flash:
        flask.flash(redirectMessage)
    if redirectPage != None:
        if not saveRedirect:
            return flask.redirect(redirectPage)
        else:
            return redirectAndSave(redirectPage)
    else:
        return function(authed=False, authMessage=redirectMessage, *args, **kwargs)

#Will return all information that is needed to render a post.
#Prevents fragmentation in various post display methods
def getPostsParameters():
    title = settings.getSettingValue("title")
    subtitle = settings.getSettingValue("subtitle")
    displayName = settings.getSettingValue("display_name")
    return {
        "blogTitle": title,
        "blogSubtitle": subtitle,
        "displayName": displayName,
    }

#Renders the theme's template if the theme contains one
#Otherwise, it renders the default template
def renderPosts(defaultPath, pageTitle, pageNumber, pageCount, nextPageExists, basePageUrl="", *args, **kwargs):
    theme = themes.getCurrentTheme()
    template = theme["template"]
    postParams = getPostsParameters()
    #Merge postParams and kwargs
    #Anything in kwargs will overwrite postParams (which is why we use these two lines)
    postParams.update(kwargs)
    kwargs = postParams

    if template == None:
        templateFile = open(defaultPath, "r")
        template = templateFile.read()
        templateFile.close()

    return flask.render_template_string(template, pageTitle=pageTitle,
        pageNumber=pageNumber, pageCount=pageCount,
        nextPageExists=nextPageExists, basePageUrl=basePageUrl,
        *args, **kwargs)

def _xssFilter(postBody):
    whitelistedTags = ["div", "span", "b", "i", "u", "a", "p", "img", "code",
                        "ul", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre"]
    #src and href must be checked seperately
    whitelistedAttributes = ["id", "class"]
    soupedBody = bs4.BeautifulSoup(postBody, "html.parser")
    blockedTags = soupedBody.findAll(lambda tag: tag.name not in whitelistedTags)
    #Check if element has any attriutes that are not allowed, but only if
    #they are not already in blockedTags. Those will be escaped, anyway.
    blockedAttrs = soupedBody.findAll(lambda tag:
                        len(set(tag.attrs.keys()) - set(whitelistedAttributes)) != 0
                        and tag.name in whitelistedTags)
    for tag in blockedTags:
        #Beautiful soup will escape HTML strings
        tag.replace_with(str(tag))

    for tag in blockedAttrs:
        allowedAttrs = {}
        for attr in tag.attrs:
            if attr in whitelistedAttributes:
                allowedAttrs[attr] = tag.attrs[attr]
            elif attr == "src" or attr == "href":
                scheme = urllib.parse.urlparse(tag.attrs[attr]).scheme
                if scheme != "data" and scheme != "javascript":
                    allowedAttrs[attr] = tag.attrs[attr]
        tag.attrs = allowedAttrs
