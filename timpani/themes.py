import os
import os.path
from . import database

THEME_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../themes"))

def getCurrentTheme():
    databaseConnection = database.ConnectionManager.getConnection("main")
    query = (databaseConnection.session
        .query(database.tables.Setting)
        .filter(database.tables.Setting.name == "theme"))
    if query.count() > 0:
        themeName = query.first().value
        themes = os.listdir(THEME_PATH)	
        folderName = None
        try:
            folderName = next(theme for theme in themes if theme.lower() == themeName.lower())
        except StopIteration:
            return None

        themePath = os.path.join(THEME_PATH, folderName, "theme.css")
        templatePath = os.path.join(THEME_PATH, folderName, "template.html")
        template = None #If this is None, the default template can be used.
        if os.path.isfile(templatePath):
            templateFile = open(templatePath, "r")
            template = templateFile.read()
            templateFile.close()

        staticPath = os.path.join(THEME_PATH, folderName, "static")
        if not os.path.isdir(staticPath):
            staticPath = None
        
        return {"template": template, "staticPath": staticPath}

def getAvailableThemes():
    files = os.listdir(THEME_PATH)
    for item in files:
        path = os.path.join(THEME_PATH, item)
        if not os.path.isdir(path):
            files.remove(item)
    return files
