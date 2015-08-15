import webserver

def start():
	#init webserver
	server = webserver.WebServer()
	application = server.run()

if __name__ == "__main__":
	start()
