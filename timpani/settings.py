from . import database

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
	databaseConnection = database.ConnectionManager.getConnection("main")
	settingObj = database.tables.Setting(name = name, value = value)
	databaseConnection.session.merge(settingObj)
	databaseConnection.session.commit()
