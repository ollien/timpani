import bcrypt
import sys
sys.path.insert(0, "..")
import timpani

connection = timpani.database.DatabaseConnection())
timpani.database.ConnectionManager.addConnection("main", connection)
hashedPassword = bcrypt.hashpw(bytes("password", "utf-8"), bcrypt.gensalt()).decode("utf-8")
timpani.auth.createUser("tests", hashedPassword, True, True)
connection.close()
