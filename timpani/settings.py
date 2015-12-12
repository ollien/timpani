from . import database
from . import themes

DEFAULT_SETTINGS = {
	"title": "Timpani",
	"subtitle": "Your blog, run using Timpani.",
	"display_name": "full_name",
	"theme": "default"
}

#Contains lambda functions that return true when the condition is valid
#Name of the game is keep them simple
SETTING_VALIDATIONS = {
	"title": lambda x: len(x) > 0,
	"display_name": lambda x: x == "full_name" or x == "username",
	"theme": lambda x: x in themes.getAvailableThemes()
}

#Messages to be returned when paramaters are found to be invalid
VALIDATION_MESAGES = {
	"title": "Title must have a length greater than zero.",
	"display_name": "Invalid display name.",
	"theme": "Invalid theme selection."
}

def getAllSettings():
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.Setting)
	settings = query.all()
	return {setting.name: setting.value for setting in settings}

def getSettingValue(name):
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = (databaseConnection.session
		.query(database.tables.Setting)
		.filter(database.tables.Setting.name == name))
	if query.count() > 0:
		return query.first().value
	return None

def setSettingValue(name, value):
	valid = validateSetting(name, value)
	if valid:
		databaseConnection = database.ConnectionManager.getConnection("main")
		settingObj = database.tables.Setting(name = name, value = value)
		databaseConnection.session.merge(settingObj)
		databaseConnection.session.commit()
		return True
	return False

def validateSetting(name, value):
	if name in SETTING_VALIDATIONS:
		return SETTING_VALIDATIONS[name](value)
	return True
