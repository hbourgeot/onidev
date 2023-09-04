from . import models, schemas
from sqlalchemy.orm import Session

def get_posts(db: Session, skip: int = 0, limit: int = 1000):
  return db.query(models.Post).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
  return db.query(models.Post).filter(models.Post.id == post_id)

def create_post(db: Session, post: schemas.Post, poster: int):
  db_post = models.Post(**post.model_dump(), original_poster=poster)
  db.add(db_post)
  db.commit()
  db.refresh(db_post)
  return db_post

