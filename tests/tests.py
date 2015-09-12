from selenium import webdriver
import tests

username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]
capabilities["tunnel-identifier"] = os.environ["TRAVIS_JOB_NUMBER"]
capabilities["build"] = os.environ["TRAVIS_BUILD_NUMBER"]
url = "%s:%s@localhost:4445" % (username, access_key)
driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % url)

tests.login.test(driver, "tests", "password")
driver.add_cookie({"name": "sessionId", "value": ""})
tests.addpost.test(driver, "tests", "password")
