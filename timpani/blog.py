from . import database
from . import configmanager
import sqlalchemy
import sqlalchemy.orm

def getMainConnection():
	return database.ConnectionManager.getConnection("main")

#Groups posts and tags in posts dict.
#Will be a dict formatted as such:
#{postId: {post: $POST_OBJECT_FROM_DATABASE, tags: [$TAGS_FROM_DATABASE]}
def _getDictFromJoin(results):
	posts = {}
	for result in results:
		post, tag = result
		if post.id in posts.keys():
			posts[post.id]["tags"].append(tag)
		else:
			posts[post.id] = {"post": post, "tags": []}
			if tag != None:
				posts[post.id]["tags"].append(tag)

	return sorted(
			list(posts.values()),
			key = lambda x: x["post"].time_posted,
			reverse = True)


def getPosts(limit = None, offset = 0, tags = True, connection = None):
	#Functions are not re-run if they are default arguments.
	if connection == None:
		connection = getMainConnection()
	if tags:
		#Gets all the posts using a join. 
		#We won't use getPostById in a loop to prevent many queries.

		#Subquery to get all posts within our limit
		postQuery = (connection.session
			.query(database.tables.Post)
			.order_by(sqlalchemy.desc(database.tables.Post.time_posted))
			.limit(limit)
			.offset(offset)
			.subquery())

		postAlias = sqlalchemy.orm.aliased(database.tables.Post, postQuery)

		#Outerjoin these together
		query = (connection.session
			.query(postAlias, database.tables.Tag)
			.outerjoin(database.tables.Tag)
			.order_by(database.tables.Tag.id))
			
		postsAndTags = query.all()

		return _getDictFromJoin(postsAndTags)

	else:
		posts = connection.session.query(database.tables.Post).all()
		return sorted(posts, key = lambda x: x.id, reverse = True)

#Gets a post form the database
#Returns None if there is no post with such an id
def getPostById(postId, tags = True, connection = None):
	if connection == None:
		connection = getMainConnection()
	if tags:
		postsAndTags = (connection.session
			.query(database.tables.Post, database.tables.Tag)
			.outerjoin(database.tables.Tag)
			.filter(database.tables.Post.id == postId).order_by(database.tables.Tag.id)
			.all())

		if len(postsAndTags) == 0:
			return None

		return {
				"post": postsAndTags[0][0],
				"tags": [item[1] for item in postsAndTags if item[1] != None]
			}
	else:
		return (connection.session.query(database.tables.Post)
			.filter(database.tables.Post.id == postId)
			.first())

def getPostsWithTag(tag, limit = None, offset = 0, tags = True, connection = None):
	if connection == None:
		connection = getMainConnection()
	if tags:

		postQuery = (connection.session
			.query(sqlalchemy.distinct(database.tables.Tag.post_id))
			.select_from(database.tables.Post)
			.join(database.tables.Tag, database.tables.Tag.post_id == database.tables.Post.id)
			.filter(database.tables.Tag.name == tag.lower())
			.limit(limit)
			.offset(offset)
			.subquery())

		query = (connection.session
			.query(database.tables.Post, database.tables.Tag)	
			.join(database.tables.Tag)
			.filter(database.tables.Post.id.in_(postQuery))
		)


		postsAndTags = query.all()

		return _getDictFromJoin(postsAndTags)

	else:
		posts = (connection.session
			.query(database.tables.Post)
			.join(database.tables.Tag)
			.filter(sqlalchemy.func.lower(database.tables.Tag.name) == tag.lower()))
		return posts.all()

def addPost(title, body, time_posted, author, tags, connection = None):
	#Functions are not re-run if they are default arguments.
	if connection == None:
		connection = getMainConnection()

	if type(tags) == str:
		tags = tags.split(" ")
	#Create the post object
	post = database.tables.Post(
		title = title,
		body = body, 
		time_posted = time_posted, 
		author = author) 

	connection.session.add(post)
	connection.session.flush()
	#Parse the tags and add them to the table
	for tag in tags:
		if len(tag) > 0:
			tag = database.tables.Tag(post_id = post.id, name = tag)
			connection.session.add(tag)
	connection.session.commit()

def editPost(postId, title, body, tags, connection = None):
	if connection == None:
		connection = getMainConnection()

	if type(tags) == str:
		tags = tags.split(" ")
	
	post = getPostById(postId)["post"]
	post.title = title
	post.body = body
	
	currentTags = (connection.session
		.query(database.tables.Tag)
		.filter(database.tables.Tag.post_id == postId))

	for tag in currentTags:
		if tag.name not in currentTags:
			connection.session.delete(tag)

	connection.session.flush()	
	currentTagNames = (connection.session
		.query(database.tables.Tag.name)
		.filter(database.tables.Tag.post_id == postId))

	for tag in tags:
		if len(tag) > 0 and tag not in currentTagNames:
			tag = database.tables.Tag(post_id = post.id, name = tag)
			connection.session.add(tag)

	connection.session.commit()
	
def deletePost(post, connection = None):
	if connection == None:
		connection = getMainConnection()

	if type(post) == int:
		post = getPostById(post, tags = False)

	if type(post) != database.tables.Post:
		raise ValueError("post must be of type int or Post, not %s" % type(post))
			
	connection.session.delete(post)	
	connection.session.commit()
