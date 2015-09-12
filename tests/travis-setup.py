import bcrypt
import sys
import os
sys.path.insert(0, "..")
import database

os.chdir("..")
connection = database.DatabaseConnection()
user = databse.tables.User("tests", "Timpani Tests", "password", True, True)
connection.session.add(user)
connection.session.commit()
connection.close()
