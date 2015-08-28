import database
import configmanager

mainConnection = database.ConnectionManager.getConnection("main")

def getPosts(connection = mainConnection):
	posts = {} #Will be a dict formatted as such {postId: {post: $POST_OBJECT_FROM_DATABASE, tags: [$TAGS_FROM_DATABASE]}}
	postsAndTags = connection.session.query(database.tables.Post, database.tables.Tag).outerjoin(database.tables.TagRelation, database.tables.Tag)
	for result in postsAndTags:
		post, tag = result
		if post.id in posts.keys():
			posts[post.id]["tags"].append(tag)
		else:
			posts[post.id] = {"post": post, "tags": []}
			if tag != None:
				posts[post.id]["tags"].append(tag)
	return posts
