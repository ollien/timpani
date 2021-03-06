import binascii
import os
import sqlalchemy
import selenium
from selenium.webdriver.common import keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from timpani import database

LOGIN_TITLE = "Login - Timpani"
ADD_POST_TITLE = "Add Post - Timpani"
#A random constant used to varify that a unique post was made
POST_RANDOM = binascii.hexlify(os.urandom(16)).decode() 
POST_TITLE = "Test post, please ignore."
POST_BODY = ("This is a test post. "
    "There is no reason you should be paying attention to it. %s" % POST_RANDOM)
POST_TAGS = ["test", "post", "selenium"]

def test(driver, username, password):
    databaseConnection = database.DatabaseConnection()
    driver.get("http://127.0.0.1:8080/add_post")	

    (WebDriverWait(driver, 10)
        .until(expected_conditions.title_contains("Timpani")))

    #Check that we were redirected to the login page, as we are not logged in.	
    assert driver.title == LOGIN_TITLE, "Title is %s" % driver.title

    loginForm = driver.find_element_by_id("login-form")
    usernameField = driver.find_element_by_id("username-field")
    passwordField = driver.find_element_by_id("password-field")
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    loginForm.submit()

    (WebDriverWait(driver, 10)
        .until_not(expected_conditions.title_is(LOGIN_TITLE)))

    #We should have been redirected to the add_post page.
    assert driver.title == ADD_POST_TITLE, "Title is %s" % driver.title
 
    postForm = driver.find_element_by_id("post-form")
    titleInput = driver.find_element_by_id("title-input")
    editorField = driver.find_element_by_css_selector("#editor > .ql-editor")
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

    post = (databaseConnection.session
        .query(database.tables.Post)
        .order_by(sqlalchemy.desc(database.tables.Post.time_posted))
        .first())
    tags = (databaseConnection.session
        .query(database.tables.Tag.name)
        .join(database.tables.TagRelation, 
            database.tables.TagRelation.tag_id == database.tables.Tag.id)
        .filter(database.tables.TagRelation.post_id == post.id)
        .all())

    #Resolve sqlalchemy tuples
    tags = [tag[0] for tag in tags]

    assert post != None
    assert post.title == POST_TITLE, "Title is %s" % post.title
    assert POST_RANDOM in post.body
    assert tags == POST_TAGS, "Tags are %s" % tags
