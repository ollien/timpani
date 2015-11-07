import selenium
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from timpani import database

def test(driver):
	databaseConnection = database.DatabaseConnection()
	driver.get("http://127.0.0.1:8080")
	#Test individual post
	permalink = driver.find_element_by_css_selector("a.timestamp-link")
	permalink.click()
	postElement = driver.find_element_by_css_selector("li.post")
	postId = postElement.get_attribute("post-id")
	query = (databaseConnection.session
		.query(database.tables.Post)
		.filter(database.tables.Post.id == postId))

	assert query.count() > 0

	post = query.first()
	titleElement = postElement.find_element_by_css_selector("h2.post-title")
	assert titleElement.text == post.title

