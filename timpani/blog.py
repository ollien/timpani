from . import database
from . import configmanager
import sqlalchemy
import sqlalchemy.orm
import math

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

def _getPostQuery(limit = None, offset = 0, tags = True, connection = None):
	if connection == None:
		connection = database.ConnectionManager.getMainConnection()
	if tags:
		#Gets all the posts using a join. 
		#We won't use getPostById in a loop to prevent many queries.

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
			.outerjoin(database.tables.TagRelation,
				postAlias.id == database.tables.TagRelation.post_id)
			.outerjoin(database.tables.Tag,
				database.tables.Tag.id == database.tables.TagRelation.tag_id)
			.order_by(database.tables.Tag.id))
			
		return query
	else:
		query = (connection.session
			.query(database.tables.Post)
			.limit(limit)
			.offset(offset))

		return query

def getPosts(limit = None, offset = 0, tags = True, connection = None):
	query = _getPostQuery(limit, offset, tags, connection)
	posts = query.all()

	if tags:
		return _getDictFromJoin(posts)
	else:
		return sorted(posts, key = lambda x: x.time_posted, reverse = True)

def getPostCount(limit = None, offset = 0, connection = None):
	query = _getPostQuery(limit, offset, False, connection)
	return query.count()

#Gets a post form the database
#Returns None if there is no post with such an id
def getPostById(postId, tags = True, connection = None):
	if connection == None:
		connection = database.ConnectionManager.getMainConnection()
	if tags:
		postsAndTags = (connection.session
			.query(database.tables.Post, database.tables.Tag)
			.outerjoin(database.tables.TagRelation,
				database.tables.Post.id == database.tables.TagRelation.post_id)
			.outerjoin(database.tables.Tag,
				database.tables.Tag.id == database.tables.TagRelation.tag_id)
			.filter(database.tables.Post.id == postId)
			.order_by(database.tables.Tag.id)
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

def _getPostsWithTagQuery(tag, limit = None, offset = 0, tags = True, connection = None):
	if connection == None:
		connection = database.ConnectionManager.getMainConnection()

	postQuery = (connection.session
		.query(database.tables.Post)
		.order_by(sqlalchemy.desc(database.tables.Post.time_posted))
		.limit(limit)
		.offset(offset)
		.subquery())

	postAlias = sqlalchemy.orm.aliased(database.tables.Post, postQuery)

	#If we're getting tags, we don't need to do anything else
	#Performing a subquery on 'postAlias' has too many columns
	baseQuery = (connection.session.query(postAlias.id) 
		if tags else connection.session.query(postAlias))

	postWithTagQuery = (baseQuery
		.join(database.tables.TagRelation, 
			database.tables.TagRelation.post_id == postAlias.id)
		.join(database.tables.Tag,
			database.tables.Tag.id == database.tables.TagRelation.tag_id)
		.filter(database.tables.Tag.name == tag)
		.order_by(database.tables.Tag.id))

	if tags:
		postWithTagQuery = postWithTagQuery.subquery()
		query = (connection.session
			.query(postAlias, database.tables.Tag)	
			.outerjoin(database.tables.TagRelation,
				postAlias.id == database.tables.TagRelation.post_id)
			.outerjoin(database.tables.Tag,
				database.tables.Tag.id == database.tables.TagRelation.tag_id)
			.filter(postAlias.id.in_(postWithTagQuery))
			.order_by(database.tables.Tag.id)
		)
		return query

	return postWithTagQuery

def getPostsWithTag(tag, limit = None, offset = 0, tags = True, connection = None):
	query = _getPostsWithTagQuery(tag, limit, offset, tags, connection)
	posts = query.all()

	if tags:
		return _getDictFromJoin(posts)
	else:
		return sorted(posts, key = lambda x: x.time_posted, reverse = True)

def getPostWithTagCount(tag, limit = None, offset = 0, connection = None):
	query = _getPostsWithTagQuery(tag, limit, offset, False, connection)
	return query.count()

def nextPageExists(postCount, pageLimit, pageNumber):
	return getPageCount(postCount, pageLimit) > pageNumber 

def getPageCount(postCount, pageLimit):
	return int(math.ceil(postCount/pageLimit))
	
def addPost(title, body, time_posted, author, tags, connection = None):
	#Functions are not re-run if they are default arguments.
	if connection == None:
		connection = database.ConnectionManager.getMainConnection()

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
	tagQuery = (connection.session
		.query(database.tables.Tag.id, database.tables.Tag.name)
		.filter(database.tables.Tag.name.in_(tags)))
	storedTags = {tag.name: tag.id for tag in tagQuery.all()}

	#Parse the tags and add them to the table
	for tag in tags:
		if len(tag) > 0:
			tagId = -1
			if tag not in storedTags:
				tag = database.tables.Tag(name = tag)
				connection.session.add(tag)
				#Without a flush, tagId will be None
				connection.session.flush()
				tagId = tag.id
			else:
				tagId = storedTags[tag]
			tagRelation = database.tables.TagRelation(post_id = post.id, tag_id = tagId)
			connection.session.add(tagRelation)
	connection.session.commit()

def editPost(postId, title, body, tags, connection = None):
	if connection == None:
		connection = database.ConnectionManager.getMainConnection()

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
		connection = database.ConnectionManager.getMainConnection()

	if type(post) == int:
		post = getPostById(post, tags = False)

	if type(post) != database.tables.Post:
		raise ValueError("post must be of type int or Post, not %s" % type(post))
			
	connection.session.delete(post)	
	connection.session.commit()
