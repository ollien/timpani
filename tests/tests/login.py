from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from termcolor import cprint

LOGIN_TITLE = "Login - Timpani"
MANAGE_TITLE = "Manage Blog - Timpani"

def test(driver, username, password):
	driver.get("http://127.0.0.1:8080/login")

	WebDriverWait(driver, 10).until(expected_conditions.title_contains("Timpani"))
	
	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys("." if username != "." else ",")
	passwordField.send_keys("." if password != "." else ",")
	loginForm.submit()

	#Will throw a timeout exception if the page doesn't load, or it can't find the element.
	WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "error")))

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(username)
	passwordField.send_keys(password)
	loginForm.submit()

	WebDriverWait(driver, 10).until_not(expected_conditions.title_is(LOGIN_TITLE))

	assert driver.title == MANAGE_TITLE, "Title is %s" % driver.title

	cprint("Login test passed!", "green")
