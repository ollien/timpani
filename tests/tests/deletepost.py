import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from timpani import database

LOGIN_TITLE = "Login - Timpani"
MANAGE_POSTS_TITLE = "Manage Posts - Timpani"

def test(driver, username, password):
    databaseConnection = database.DatabaseConnection()
    driver.get("http://127.0.0.1:8080/manage_posts")
    (WebDriverWait(driver, 10)
        .until(expected_conditions.title_contains("Timpani")))

    #Check that we are on the login page, we shouldn't be logged in.
    assert driver.title == LOGIN_TITLE, "Title is {}".format(driver.title)

    loginForm = driver.find_element_by_id("login-form")
    usernameField = driver.find_element_by_id("username-field")
    passwordField = driver.find_element_by_id("password-field")
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    loginForm.submit()
    (WebDriverWait(driver, 10)
        .until_not(expected_conditions.title_is(LOGIN_TITLE)))

    assert driver.title == MANAGE_POSTS_TITLE, "Title is {}".format(driver.title)

    firstPost = driver.find_element_by_css_selector("li.post")
    postId = firstPost.get_attribute("post-id")
    #Confirm this post is in the database
    query = (databaseConnection.session
        .query(database.tables.Post)
        .filter(database.tables.Post.id == postId))

    assert query.count() == 1

    deleteButton = firstPost.find_element_by_css_selector("a.button.delete")
    confirmDeleteButton = driver.find_element_by_css_selector("button.positive.delete")
    deleteButton.click()

    (WebDriverWait(driver, 10)
        .until(expected_conditions.element_to_be_clickable(("css selector", "button.positive.delete"))))

    confirmDeleteButton.click()

    #The request has finished when the post li has disappeared, so wait for it
    (WebDriverWait(driver, 10)
        .until(expected_conditions.invisibility_of_element_located(
            ("css selector", "li.post[post-id='{}']".format(postId)))))
    assert query.count() == 0, query.count()
