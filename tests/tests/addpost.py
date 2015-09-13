import sqlalchemy
import selenium
from selenium.webdriver.common import keys
from termcolor import cprint
from timpani import database

POST_TITLE = "Test post, please ignore."
POST_BODY = "This is a test post. There is no reason you should be paying attention to it."
POST_TAGS = ["test", "post", "selenium"]

def test(driver, username, password):
	databaseConnection = database.DatabaseConnection()
	driver.get("http://127.0.0.1:8080/add_post")	
	#Check that we were redirected to the login page, as we are not logged in.	
	assert driver.title == "Login - Timpani", "Title is %s" % driver.title

	loginForm = driver.find_element_by_id("login-form")
	usernameField = driver.find_element_by_id("username-field")
	passwordField = driver.find_element_by_id("password-field")
	usernameField.send_keys(username)
	passwordField.send_keys(password)
	loginForm.submit()
	#We should have been redirected to the add_post page.
	assert driver.title == "Add Post - Timpani", "Title is %s" % driver.title
 

	postForm = driver.find_element_by_id("post-form")
	titleInput = driver.find_element_by_id("title-input")
	editorField = driver.find_element_by_id("editor")
	tagsInput = driver.find_element_by_id("tag-input-div")

	titleInput.click()
	titleInput.send_keys(POST_TITLE)
	
	editorField.click()
	actionChain = selenium.webdriver.ActionChains(driver)
	actionChain.send_keys(POST_BODY)
	actionChain.perform()

	tagsInput.click()
	actionChain = selenium.webdriver.ActionChains(driver)
	for tag in POST_TAGS:
		actionChain.send_keys(tag)
		actionChain.send_keys(keys.Keys.SPACE)
	actionChain.perform()
	
	postForm.submit()

	post = databaseConnection.session.query(database.tables.Post).order_by(sqlalchemy.desc(database.tables.Post.id)).first()
	tags = databaseConnection.session.query(database.tables.Tag.name).filter(database.tables.Tag.post_id == post.id).all()
	tags = [tag[0] for tag in tags] #Resolve sqlalchemy tuples

	assert post != None
	assert post.title == POST_TITLE, "Title is %s" % post.title
	assert tags == POST_TAGS, "Tags are %s" % tags

	cprint("add_post test passed!", "green")
