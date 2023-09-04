from pydantic import BaseModel

class DevBase(BaseModel):
  email: str

class Dev(DevBase):
  id: int
  hashed_password: str
  name: str

  class Config:
    orm_mode = True

class Post(BaseModel):
  id: int
  text: str
  likes: int
  original_poster: int

  class Config:
    orm_mode = True

class Hashtag(BaseModel):
  id: int
  tag: str

  class Config:
    orm_mode = True

class Comment(BaseModel):
  id: int
  text: str
  likes: int
  dev_id: int

  class Config:
    orm_mode = True