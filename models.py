from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

followers_table = Table(
  'followers', Base.metadata, Column('follower_id', Integer, ForeignKey('devs.id'), primary_key=True), Column('followed_id', Integer, ForeignKey('devs.id'), primary_key=True)
)

post_hashtags_table = Table(
    'post_hashtags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('hashtag_id', Integer, ForeignKey('hashtags.id'), primary_key=True)
)

class Dev(Base):
  __tablename__ = "devs"
  
  id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
  email = Column(String, unique=True, index=True)
  hashed_password = Column(String)
  name = Column(String(80))
  
  followed = relationship('Dev', secondary=followers_table, primaryjoin=followers_table.c.follower_id == id, secondaryjoin=followers_table.c.follower_id == id,backref="followers")
  
  posts = relationship('Post', back_populates='original_poster')
  comments = relationship('Comment', back_populates='dev')

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True, index=True, autoincrement="auto")
  text = Column(String(500))
  likes = Column(Integer)
  dev_id = Column(Integer, ForeignKey("devs.id"))
  
  original_poster = relationship('Dev', back_populates='posts')
  hashtags = relationship('Hashtags', secondary=post_hashtags_table, back_populates='posts')
  comments = relationship('Comment', back_populates='post')

class Hashtags(Base):
  __tablename__ = "hashtags"
  
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  tag = Column(String(30), unique=True)

  posts = relationship('Post', secondary=post_hashtags_table, back_populates='hashtags')
  
class Comment(Base):
  __tablename__ = "comments"
  
  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  text = Column(String(300))
  likes = Column(Integer)
  dev_id = Column(Integer, ForeignKey("devs.id"))

  dev = relationship('Dev', back_populates='comments')
  post = relationship('Post', back_populates='comments')
    