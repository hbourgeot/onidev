from . import models, schemas
from sqlalchemy.orm import Session

from sqlalchemy.orm import Session
from . import models, schemas

# ------------ CRUD para Dev -------------

def create_dev(db: Session, dev: schemas.DevCreate):
    db_dev = models.Dev(**dev.dict())
    db.add(db_dev)
    db.commit()
    db.refresh(db_dev)
    return db_dev

def get_devs(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Dev).offset(skip).limit(limit).all()

def get_dev_by_id(db: Session, dev_id: int):
    return db.query(models.Dev).filter(models.Dev.id == dev_id).first()

def update_dev(db: Session, dev_id: int, dev: schemas.DevCreate):
    db_dev = db.query(models.Dev).filter(models.Dev.id == dev_id).first()
    if db_dev is None:
        return None
    for key, value in dev.dict().items():
        setattr(db_dev, key, value)
    db.commit()
    db.refresh(db_dev)
    return db_dev

# ------------ CRUD para Post -------------

def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def update_post(db: Session, post_id: int, post: schemas.PostCreate):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    for key, value in post.dict().items():
        setattr(db_post, key, value)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        return None
    db.delete(db_post)
    db.commit()
    return db_post
# ------------ CRUD para Hashtag -------------

def create_hashtag(db: Session, hashtag: schemas.Hashtag):
    db_hashtag = models.Hashtags(**hashtag.dict())
    db.add(db_hashtag)
    db.commit()
    db.refresh(db_hashtag)
    return db_hashtag

def get_hashtags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Hashtags).offset(skip).limit(limit).all()

# ------------ CRUD para Comment -------------

def create_comment(db: Session, comment: schemas.Comment):
    db_comment = models.Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def update_comment(db: Session, comment_id: int, comment: schemas.Comment):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        return None
    for key, value in comment.dict().items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        return None
    db.delete(db_comment)
    db.commit()
    return db_comment