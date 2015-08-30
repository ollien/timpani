import collections
import database
import configmanager

def getMainConnection():
	return database.ConnectionManager.getConnection("main")

def getPosts(connection = None):
	#Functions are not re-run if they are default arguments.
	if connection == None:
		connection = getMainConnection()
	posts = {} #Will be a dict formatted as such {postId: {post: $POST_OBJECT_FROM_DATABASE, tags: [$TAGS_FROM_DATABASE]}
	postsAndTags = connection.session.query(database.tables.Post, database.tables.Tag).outerjoin(database.tables.Tag).filter(database.tables.Post != None).all()
	#Groups posts and tags in posts dict.
	for result in postsAndTags:
		post, tag = result
		if post.id in posts.keys():
			posts[post.id]["tags"].append(tag)
		else:
			posts[post.id] = {"post": post, "tags": []}
			if tag != None:
				posts[post.id]["tags"].append(tag)

	return sorted(list(posts.values()), key = lambda x: x["post"].time_posted, reverse = True)

def addPost(title, body, time_posted, author, tags, connection = None):
	#Functions are not re-run if they are default arguments.
	if connection == None:
		connection = getMainConnection()
	if type(tags) == str:
		tags = tags.split(" ")
	#Create the post object
	post = database.tables.Post(title = title, body = body, time_posted = time_posted, author = author) 
	connection.session.add(post)
	connection.session.flush()
	#Parse the tags, and add them to the relations table for our many to many relationship.
	for tag in tags:
		if len(tag) > 0:
			tag = database.tables.Tag(post_id = post.id, name = tag)
			connection.session.add(tag)
	connection.session.commit()

def getAuthorUsername(user, connection = None):
	if connection == None:
		connection = getMainConnection()

	if type(user) == int:
		user = connection.session.query(database.tables.User).filter(database.tables.User.id == user).first()
	elif type(user) != database.tables.User:
		raise ValueError("User must be of type User, not %s" % type(user).__name__)

	return user.username
		
def getAuthorFullname(user, connection = None):
	if connection == None:
		connection = getMainConnection()

	if type(user) == int:
		user = connection.session.query(database.tables.User).filter(database.tables.User.id == user).first()
	elif type(user) != database.tables.User:
		raise ValueError("User must be of type User, not %s" % type(user).__name__)

	return user.full_name
