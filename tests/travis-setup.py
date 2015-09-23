import bcrypt
import sys
sys.path.insert(0, "..")
import timpani

connection = timpani.database.DatabaseConnection()
timpani.database.ConnectionManager.addConnection(connection, "main")
timpani.auth.createUser("tests", "Timpani Tests", "password", True, True)
connection.close()
