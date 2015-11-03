from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

LOGIN_TITLE = "Login - Timpani"
MANAGE_TITLE = "Manage Blog - Timpani"

def test(driver, username, password):
	driver.get("http://127.0.0.1:8080/login")

	(WebDriverWait(driver, 10)
		.until(expected_conditions.title_contains("Timpani")))
	
	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(username)
	passwordField.send_keys(password)
	loginForm.submit()

	(WebDriverWait(driver, 10)
		.until_not(expected_conditions.title_is(LOGIN_TITLE)))

	assert driver.title == MANAGE_TITLE, "Title is %s" % driver.title

	logoutButton = driver.find_element_by_css_selector("button.logout-button")
	logoutButton.click()

	(WebDriverWait(driver, 10)
		.until_not(expected_conditions.title_is(MANAGE_TITLE)))

	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

	#Check that the user has no session in their cache.
	#This can be confirmed by accessing a restricted page,
	#such as manage.
	driver.get("http://127.0.0.1:8080/manage")
	(WebDriverWait(driver, 10)
		.until(expected_conditions.title_contains("Timpani")))

	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title
