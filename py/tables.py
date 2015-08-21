import sqlalchemy
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class Post(Base):
	__tablename__ = "posts"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	title = sqlalchemy.Column(sqlalchemy.String)
	body = sqlalchemy.Column(sqlalchemy.Text,) #Should be text to avoid length problems
	time_posted = sqlalchemy.Column(sqlalchemy.DateTime)
	author = sqlalchemy.Column(sqlalchemy.String)

class Tag(Base):
	__tablename__ = "tags"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	name = sqlalchemy.Column(sqlalchemy.Text)

#Used to relate tags to posts.
class TagRelation(Base):
	__tablename__ = "tag_relations"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Post.__table__.columns.id))
	tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Tag.__table__.columns.id))

class User(Base):
	__tablename__ = "users"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	username = sqlalchemy.Column(sqlalchemy.String)
	password = sqlalchemy.Column(sqlalchemy.String)
	can_change_settings = sqlalchemy.column(sqlalchemy.Boolean)
	can_write_posts = sqlalchemy.column(sqlalchemy.Boolean)

#The Following tables will only be the ones added to the database
ALL_TABLES = [Post, Tag, TagRelation]
