import selenium

def test(driver, username, password):
	driver.get("http://127.0.0.1:8080/login")
	
	assert driver.title == "Login"

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys("." if username != "." else ",")
	passwordField.send_keys("." if password != "." else ",")
	loginForm.submit()
	errorDiv = None

	try:
		errorDiv = driver.find_element_by_id("error")

	except NoSuchElementException:
		#This will be asserted in a moment. It's ok to pass this.	
		pass
	
	assert errorDiv != None

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(username)
	passwordField.send_keys(password)
	loginForm.submit()

	assert driver.title == "Manage"
