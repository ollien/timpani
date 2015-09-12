import bcrypt
import sys
import os
from timpani import database

connection = database.DatabaseConnection()
user = database.tables.User(username = "tests", password = "password", full_name = "Timpani Tests", can_change_settings = True, can_write_posts = True)
connection.session.add(user)
connection.session.commit()
connection.close()
