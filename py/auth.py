import bcrypt
import database
import uuid
import datetime

def createUser(username, password, can_change_settings, can_write_posts):
	username = username.lower()
	passwordAsBytes = bytes(password, "utf-8")
	passwordHash = bcrypt.hashpw(passwordAsBytes, bcrypt.gensalt()).decode("utf-8")
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.User).filter(database.tables.User.username == username)

	if query.count() == 0:
		userObject = database.tables.User(username = username, password = passwordHash, can_change_settings = can_change_settings, can_write_posts = can_write_posts)
		databaseConnection.session.add(userObject)
		databaseConnection.session.commit()
	else:
		raise ValueError("Username is not unique.")

def validateUser(username, password):
	username = username.lower()
	passwordAsBytes = bytes(password, "utf-8")
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.User).filter(database.tables.User.username == username)

	if query.count() > 0:
		userObject = query.first()
		userPassword = bytes(userObject.password,"utf-8")
		if bcrypt.hashpw(passwordAsBytes, userPassword) == userPassword:
			return True

	return False

def createSession(username, sessionId = uuid.uuid4().hex):
	username = username.lower()
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.User).filter(database.tables.User.username == username)

	if query.count() > 0:
		userObject = query.first()
		userId = userObject.id
		expires = datetime.datetime.now() + datetime.timedelta(0, 0, 0, 0, 0, 0, 2) #Now plus two weeks.
		sessionObj = database.tables.Session(user_id = userId, session_id = sessionId, expires = expires)
		databaseConnection.session.add(sessionObj)
		databaseConnection.session.commit()
		return sessionId
	else:
		raise ValueError("username does not exist.")

def validateSession(sessionId):
	databaseConnection = database.ConnectionManager.getConnection("main")
	query = databaseConnection.session.query(database.tables.Session).filter(database.tables.Session.session_id == sessionId)

	if query.count() > 0:
		sessionObj = query.first()
		userId = sessionObj.user_id
		if datetime.datetime.now() < sessionObj.expires:
			userQuery = databaseConnection.session.query(database.tables.User).filter(database.tables.User.id == userId)
			if userQuery.count() > 0:
				return userQuery.first()

	return None
