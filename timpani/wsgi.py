from . import timpani
from . import database
import atexit

def shutdown():
	print("[Timpani] Closing database connection")
	database.ConnectionManager.closeConnection("main")

atexit.register(shutdown)

application = timpani.run(startServer = False)
