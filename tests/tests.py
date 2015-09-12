from selenium import webdriver
import tests

driver = webdriver.Chrome() #Will be replaced with selenium once test dev is finished

tests.login.test(driver, "tests", "password")
driver.add_cookie({"name": "sessionId", "value": ""})
tests.addpost.test(driver, "tests", "password")
