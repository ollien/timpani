from . import database

def getSettingValue(name):
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.Setting).filter(database.tables.Setting.name == name)
	if query.count() > 0:
		return query.first().value
	return None

def setSettingValue(name, value):
	databaseConnection = database.ConnectionManager.getConnection("main")
	settingObj = database.tables.Setting(name = name, value = value)
	databaseConnection.session.add(settingObj)
	databaseConnection.session.commit()
