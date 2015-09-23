import bcrypt
import sys
import os
sys.path.insert(0, "..")
import timpani
hashedpassword = bcrypt.hashpw(bytes("password", "utf-8"), bcrypt.gensalt()).decode("utf-8")
timpani.auth.createUser("tests", hashedPassword, True, True)
connection.close()
