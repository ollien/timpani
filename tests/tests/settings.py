import binascii
import os
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

LOGIN_TITLE = "Login - Timpani"
SETTINGS_TITLE = "Settings - Timpani"

TITLE = "Timpani! {}".format(binascii.hexlify(os.urandom(32)).decode())
SUBTITLE = ("Your subtitle, set using unit testing. {}".format(
    binascii.hexlify(os.urandom(32)).decode()))

def test(driver, username, password):
    driver.get("http://127.0.0.1:8080/settings")

    (WebDriverWait(driver, 10)
        .until(expected_conditions.title_contains("Timpani")))

    assert driver.title == LOGIN_TITLE, "Title is {}".format(driver.title)

    loginForm = driver.find_element_by_id("login-form")
    usernameField = driver.find_element_by_id("username-field")
    passwordField = driver.find_element_by_id("password-field")
    usernameField.send_keys(username)
    passwordField.send_keys(password)
    loginForm.submit()

    (WebDriverWait(driver, 10)
        .until_not(expected_conditions.title_is(LOGIN_TITLE)))

    assert driver.title == SETTINGS_TITLE, "Title is {}".format(driver.title)

    settingsForm = driver.find_element_by_id("settings-form")
    titleField = driver.find_element_by_id("blog-title-input")
    subtitleField = driver.find_element_by_id("blog-subtitle-input")
    saveButton = driver.find_element_by_id("save")
    titleField.clear()
    titleField.send_keys(TITLE)
    subtitleField.clear()
    subtitleField.send_keys(SUBTITLE)
    settingsForm.submit()

    #Will throw a timeout exception if the
    #page doesn't load, or it can't find the element.
    (WebDriverWait(driver, 10)
        .until(expected_conditions.presence_of_element_located((By.ID, "success-message"))))

    driver.get("http://127.0.0.1:8080")

    blogTitle = driver.find_element_by_css_selector("h2.title")
    blogSubtitle = driver.find_element_by_css_selector("h3.subtitles")

    assert blogTitle.text == TITLE, "Element text is {}".format(blogTitle.text)
    assert blogSubtitle.text == SUBTITLE, "Element text is {}".format(blogSubtitle.text)
