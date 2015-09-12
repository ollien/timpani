import bcrypt
import sys
import os
from timpani import database

connection = database.DatabaseConnection()
hashedpassword = bcrypt.hashpw(bytes("password", "utf-8"), bcrypt.gensalt()).decode("utf-8")
user = database.tables.User(username = "tests", password = hashedpassword, full_name = "Timpani Tests", can_change_settings = True, can_write_posts = True)
connection.session.add(user)
connection.session.commit()
connection.close()
