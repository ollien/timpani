import auth

def checkForSession(request):
	if "sessionId" in request.cookies:
		session = auth.validateSession(request.cookies["sessionId"])
		if session != None:
			return session
	return None

