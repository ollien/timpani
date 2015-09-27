import bcrypt
import sys
sys.path.insert(0, "..")
import timpani

connection = timpani.database.DatabaseConnection()
timpani.database.ConnectionManager.addConnection(connection, "main")
timpani.auth.createUser("tests", "Timpani Tests", "password", True, True)
timpani.auth.createUser("testsAuthor", "Timpani Auhtor", "password", False, True)
timpani.auth.createUser("testsAdmin", "Timpani Admin", "password", True, False)
connection.close()
