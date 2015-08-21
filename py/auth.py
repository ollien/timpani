import bcrypt
import database

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
