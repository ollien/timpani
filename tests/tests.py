from selenium import webdriver
import os
import traceback
import shutil
import tests

browsers = [
	{"browserName": "chrome", "platform": "Windows 7", "version": "45.0"},
	{"browserName": "chrome", "platform": "Windows 7", "version": "44.0"},
	{"browserName": "chrome", "platform": "Windows 7", "version": "43.0"},

	{"browserName": "firefox", "platform": "Windows 7", "version": "40.0"},
	{"browserName": "firefox", "platform": "Windows 7", "version": "39.0"},
	{"browserName": "firefox", "platform": "Windows 7", "version": "38.0"},

	{"browserName": "internet explorer", "platform": "Windows 7", "version": "11.0"},
	{"browserName": "internet explorer", "platform": "Windows 7", "version": "10.0"},

	{"browserName": "opera", "platform": "Windows 7", "version": "12.12"}
]

default_capabilities = {}
default_capabilities["javascriptEnabled"] = True
username = os.environ["SAUCE_USERNAME"]
access_key = os.environ["SAUCE_ACCESS_KEY"]
default_capabilities["tunnel-identifier"] = os.environ["TRAVIS_JOB_NUMBER"]
default_capabilities["build"] = os.environ["TRAVIS_BUILD_NUMBER"]
url = "%s:%s@localhost:4445" % (username, access_key)

def printTestResult(message, secondaryMessage, ansi):
	#Determine the number of spaces needed to float the secondary message to the right
	spaces = shutil.get_terminal_size().columns - (len(message) + len(secondaryMessage) + 2)
	print(message, end = "")
	print(" " * spaces, end = "")
	print("[%s" % ansi, end = "")
	print(secondaryMessage, end = "")
	print("%s]" % "\033[0m")

def passTest(testName):
	printTestResult(testName, "pass", "\033[92m")

def failTest(testName):
	printTestResult(testName, "fail", "\033[91m")

for browser in browsers:
	capabilities = default_capabilities.copy()
	capabilities.update(browser)
	driver = webdriver.Remote(desired_capabilities=capabilities, command_executor="http://%s/wd/hub" % url)

	print("Running tests on %s v%s" % (browser["browserName"], browser["version"]))

	#Login Test
	failed = False
	try:
		tests.login.test(driver, "tests", "password")

	except:
		traceback.print_exc()
		failed = True

	if failed:
		failTest("Login test")
	
	else:
		passTest("Login test")
		
	
	driver.add_cookie({"name": "sessionId", "value": ""})

	#Add Post Test
	failed = False
	try:
		tests.addpost.test(driver, "tests", "password")

	except:
		traceback.print_exc()
		failed = True

	if failed:
		failTest("Add post test")
	
	else:
		passTest("Add post test")

	driver.close()
	driver.quit()
