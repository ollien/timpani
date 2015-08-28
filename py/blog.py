import collections
import database
import configmanager

def getMainConnection():
	return database.ConnectionManager.getConnection("main")

mainConnection = getMainConnection() 

def getPosts(connection = mainConnection):
	global mainConnection
	if connection == mainConnection and mainConnection == None:
		mainConnection = getMainConnection()
		connection = mainConnection
	posts = collections.OrderedDict() #Will be an ordered dict formatted as such {postId: {post: $POST_OBJECT_FROM_DATABASE, tags: [$TAGS_FROM_DATABASE]}}
	postsAndTags = connection.session.query(database.tables.Post, database.tables.Tag).outerjoin(database.tables.TagRelation, database.tables.Tag).filter(database.tables.Post != None).all()
	postsAndTags.sort(key = lambda x: x[0].time_posted, reverse = True)
	#Groups posts and tags in posts dict.
	for result in postsAndTags:
		post, tag = result
		if post.id in posts.keys():
			posts[post.id]["tags"].append(tag)
		else:
			posts[post.id] = {"post": post, "tags": []}
			if tag != None:
				posts[post.id]["tags"].append(tag)
	return posts

def addPost(title, body, time_posted, author, tags, connection = mainConnection):
	global mainConnection
	if connection == mainConnection and mainConnection == None:
		mainConnection = getMainConnection()
		connection = mainConnection
	if type(tags) == str:
		tags = tags.split(" ")
	#Create the post object
	post = database.tables.Post(title = title, body = body, time_posted = time_posted, author = author) 
	connection.session.add(post)
	connection.session.flush()
	#Parse the tags, and add them to the relations table for our many to many relationship.
	for tag in tags:
		tag = database.tables.Tag(name = tag)
		connection.session.add(tag)
		connection.session.flush()
		relation = database.tables.TagRelation(post_id = post.id, tag_id = tag.id)
		connection.session.add(relation)
	connection.session.commit()
