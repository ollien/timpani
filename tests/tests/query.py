import selenium
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import sqlalchemy
from timpani import database
from timpani import settings

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

    assert query.count() == 1

    post = query.first()
    titleElement = postElement.find_element_by_css_selector("h2.post-title")

    assert titleElement.text == post.title

    driver.get("http://127.0.0.1:8080")
    tagElement = driver.find_element_by_css_selector("li.tag")
    tag = tagElement.text
    tag = tag[1:] if tag[0] == "#" else tag
    tagElement.click()
    postElements = driver.find_elements_by_css_selector("li.post")
    query = (databaseConnection.session
        .query(database.tables.TagRelation.post_id)
        .join(database.tables.Tag,
            database.tables.Tag.id == database.tables.TagRelation.tag_id)
        .join(database.tables.Post,
            database.tables.Post.id == database.tables.TagRelation.post_id)
        .filter(database.tables.Tag.name == tag.lower())
        .order_by(sqlalchemy.desc(database.tables.Post.time_posted))
        .limit(settings.getSettingValue("posts_per_page")))

    #There must be at least one post with a tag
    assert query.count() > 0 

    postIds = query.all()
    #Resolve sqlalchemy tuples
    postIds = [postId[0] for postId in postIds]

    assert len(postIds) == len(postElements)

    for postElement in postElements:
        postId = postElement.get_attribute("post-id")
        assert int(postId) in postIds
        postIds.remove(int(postId))

    assert len(postIds) == 0, "postIds is " % str(postIds)
        
