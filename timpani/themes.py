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
		theme = "" #No CSS
		if os.path.isfile(themePath):
			themeFile = open(themePath, "r")
			theme = themeFile.read()
			themeFile.close()

		templatePath = os.path.join(THEME_PATH, folderName, "template.html")
		template = None #If this is None, the default template can be used.
		if os.path.isfile(templatePath):
			templateFile = open(templatePath, "r")
			template = templatefile.read()
			templateFile.close()
		
		return {"template": template, "theme": theme}

def getAvailableThemes():
	files = os.listdir(THEME_PATH)
	for item in files:
		path = os.path.join(THEME_PATH, item)
		if not os.path.isdir(path):
			files.remove(item)
	return files
