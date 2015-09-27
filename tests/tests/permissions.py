import sqlalchemy
import selenium
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from timpani import database

LOGIN_TITLE = "Login - Timpani"
MANAGE_TITLE = "Manage Blog - Timpani"
ADD_POST_TITLE = "Add Post - Timpani"
SETTINGS_TITLE = "Settings - Timpani"

def test(driver, authorUsername, authorPassword, adminUsername, adminPassword):
	databaseConnection = database.DatabaseConnection()
	driver.get("http://127.0.0.1:8080/login")

	WebDriverWait(driver, 10).until(expected_conditions.title_contains("Timpani"))

	#Check that we were redirected to the login page, as we are not logged in.	
	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

	#Log in as author and make sure we can access addPosts, but not settings
	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(authorUsername)
	passwordField.send_keys(authorPassword)
	loginForm.submit()

	WebDriverWait(driver, 10).until_not(expected_conditions.title_is(LOGIN_TITLE))

	assert driver.title == MANAGE_TITLE, "Title is %s" % driver.title
 
	driver.get("http://127.0.0.1:8080/add_post")

	assert driver.title == ADD_POST_TITLE, "Title is %s" % driver.title

	#Settings are not yet implemented. This block will be uncommented when they are implemented.
	#driver.get("http://127.0.0.1:8080/settings")

	#assert driver.title == MANAGE_TITLE
	##Will throw a timeout exception if the page doesn't load, or it can't find the element.
	#WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.error")))

	#Log out and try the next account.
	logoutButton = driver.find_element_by_css_selector("button.logout-button")
	logoutButton.click()

	WebDriverWait(driver, 10).until(expected_conditions.title_is(LOGIN_TITLE))

	assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

	#Log in as admin and make sure we can access settings, but not addPosts
	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(adminUsername)
	passwordField.send_keys(adminPassword)
	loginForm.submit()

	WebDriverWait(driver, 10).until_not(expected_conditions.title_is(LOGIN_TITLE))
	assert driver.title == MANAGE_TITLE, "Title is %s" % driver.title

	#Settings are not yet implemented. This block will be uncommented when they are implemented.
	#driver.get("http://127.0.0.1:8080/settings")

	#assert driver.title == SETTINGS_TITLE, "Title is %s" % driver.title

	driver.get("http://127.0.0.1:8080/add_post")

	assert driver.title == MANAGE_TITLE, "Title is %s" % driver.title
	#Will throw a timeout exception if the page doesn't load, or it can't find the element.
	WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.error")))
