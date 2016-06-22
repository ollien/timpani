import bcrypt
import os
import binascii
import datetime
import sqlalchemy
from . import database
from . import configmanager

BCRYPT_ROUNDS = 10

FILE_LOCATION = os.path.abspath(os.path.dirname(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(FILE_LOCATION, "../configs/"))

configs = configmanager.ConfigManager(configPath = CONFIG_PATH)
authConfig = configs["auth"]

CAN_CHANGE_SETTINGS_PERMISSION = "can_change_settings"
CAN_POST_PERMISSION = "can_write_posts"

#Returns user object if exists, None if otherwise
def getUserById(userId):
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User)
        .filter(database.tables.User.id == userId))
    return query.first()

#Returns user object if exists, None if otherwise
def getUserByUsername(username):
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User)
        .filter(sqlalchemy.func.lower(database.tables.User.username)
            == username.lower()))
    return query.first()

#Returns list of user objects.
def getAllUsers():
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User))
    return query.all()

def createUser(username, full_name, password, can_change_settings, can_write_posts):
    passwordAsBytes = bytes(password, "utf-8")
    passwordHash = bcrypt.hashpw(passwordAsBytes,
        bcrypt.gensalt(rounds = BCRYPT_ROUNDS))
    passwordHash = passwordHash.decode("utf-8")
    databaseConnection = database.ConnectionManager.getMainConnection()
    userObject = database.tables.User(
        username = username,
        full_name = full_name,
        password = passwordHash,
        can_change_settings = can_change_settings,
        can_write_posts = can_write_posts)

    databaseConnection.session.add(userObject)
    databaseConnection.session.commit()

    return userObject

def validateUser(username, password):
    passwordAsBytes = bytes(password, "utf-8")
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User)
        .filter(sqlalchemy.func.lower(database.tables.User.username)
            == username.lower()))
    if query.count() > 0:
        userObject = query.first()
        userPassword = bytes(userObject.password,"utf-8")
        if bcrypt.hashpw(passwordAsBytes, userPassword) == userPassword:
            return True

    return False

def userHasPermission(username, permissionName):
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User)
        .filter(sqlalchemy.func.lower(database.tables.User.username) == username.lower()))

    if query.count() > 0:
        userObj = query.first()
        return getattr(userObj, permissionName)
    return False

def deleteUser(user):
    #user must be a user object
    if type(user) != database.tables.User:
        raise TypeError("user must be of type User, not {}".format(type(user).__name__))
    databaseConnection = database.ConnectionManager.getMainConnection()
    databaseConnection.session.delete(user)
    databaseConnection.session.commit()

def deleteUserById(userId):
    user = getUserById(userId)
    deleteUser(user)

def deleteUserByUsername(username):
    user = getUserByUsername(username)
    deleteUser(user)

def generateSessionId():
    sessionId = binascii.hexlify(os.urandom(authConfig["session_id_length"]))
    return sessionId.decode("utf-8")

def createSession(username, sessionId = None):
    if sessionId == None:
        sessionId = generateSessionId()
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.User)
        .filter(sqlalchemy.func.lower(database.tables.User.username)
            == username.lower()))

    if query.count() > 0:
        userObject = query.first()
        userId = userObject.id
        #Set expiry to the date of now + two weeks
        expires = datetime.datetime.now() + datetime.timedelta(weeks = 2)
        sessionObj = database.tables.Session(
            user_id = userId,
            session_id = sessionId,
            expires = expires)
        databaseConnection.session.add(sessionObj)
        databaseConnection.session.commit()
        return (sessionId, expires)
    else:
        raise ValueError("username does not exist.")

def validateSession(sessionId):
    databaseConnection = database.ConnectionManager.getMainConnection()
    query = (databaseConnection.session
        .query(database.tables.Session)
        .filter(database.tables.Session.session_id == sessionId))

    if query.count() > 0:
        sessionObj = query.first()
        userId = sessionObj.user_id
        if datetime.datetime.now() < sessionObj.expires:
            userQuery = (databaseConnection.session
                .query(database.tables.User)
                .filter(database.tables.User.id == userId))
            if userQuery.count() > 0:
                return sessionObj

    return None

def invalidateSession(sessionId):
    databaseConnection = database.ConnectionManager.getMainConnection()
    #Delete the session from the database
    query = (databaseConnection.session
        .query(database.tables.Session)
        .filter(database.tables.Session.session_id == sessionId)
        .delete(synchronize_session=False))
