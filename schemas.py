from pydantic import BaseModel
from typing import List, Optional
class DevBase(BaseModel):
  email: str

class Dev(DevBase):
  id: Optional[int]
  hashed_password: str
  name: str

  followed: Optional[List[int]]
  followers: Optional[List[int]]

  class Config:
    orm_mode = True

class Post(BaseModel):
  id: Optional[int]
  text: str
  likes: int
  original_poster: int
  hashtags: Optional[List[int]]
  comments: Optional[List[int]]

  class Config:
    orm_mode = True

class Hashtag(BaseModel):
  id: Optional[int]
  tag: str
  posts: Optional[List[int]]

  class Config:
    orm_mode = True

class Comment(BaseModel):
  id: Optional[int]
  text: str
  likes: int
  dev_id: int
  post_id: int

  class Config:
    orm_mode = True