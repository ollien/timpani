import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

Base = sqlalchemy.ext.declarative.declarative_base()

class User(Base):
	__tablename__ = "users"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	username = sqlalchemy.Column(sqlalchemy.String, unique = True, nullable = False)
	full_name = sqlalchemy.Column(sqlalchemy.String, nullable = False)
	password = sqlalchemy.Column(sqlalchemy.String, nullable = False)
	can_change_settings = sqlalchemy.Column(sqlalchemy.Boolean)
	can_write_posts = sqlalchemy.Column(sqlalchemy.Boolean)

	__table_args__ = (
		sqlalchemy.schema.Index("username_unique", sqlalchemy.func.lower(username), unique = True),
	)


class Post(Base):
	__tablename__ = "posts"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	title = sqlalchemy.Column(sqlalchemy.String)
	body = sqlalchemy.Column(sqlalchemy.Text,) #Should be text to avoid length problems
	time_posted = sqlalchemy.Column(sqlalchemy.DateTime)
	author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.__table__.columns.id))
	author = sqlalchemy.orm.relationship("User", foreign_keys = author_id)	

class Tag(Base):
	__tablename__ = "tags"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	name = sqlalchemy.Column(sqlalchemy.Text, unique = True, nullable = False)

class TagRelation(Base):
	__tablename__ = "tag_relations"

	post_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Post.__table__.columns.id, ondelete = "CASCADE"), primary_key = True)
	tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Tag.__table__.columns.id, ondelete = "CASCADE"), primary_key = True)
	post = sqlalchemy.orm.relationship("Post", foreign_keys = post_id)
	tag = sqlalchemy.orm.relationship("Tag", foreign_keys = tag_id)

class Session(Base):
	__tablename__ = "sessions"

	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True)
	user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(User.__table__.columns.id))
	user = sqlalchemy.orm.relationship("User", foreign_keys = user_id)
	session_id = sqlalchemy.Column(sqlalchemy.String, nullable = False, index = True)
	expires = sqlalchemy.Column(sqlalchemy.DateTime, nullable = False)

class Setting(Base):
	__tablename__ = "settings"
	
	name = sqlalchemy.Column(sqlalchemy.String, primary_key = True)
	value = sqlalchemy.Column(sqlalchemy.String)
