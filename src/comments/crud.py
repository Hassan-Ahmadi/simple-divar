from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas, exceptions


def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_comments_by_user_id(db: Session, user_id: int):
    return db.query(models.Comment).filter(models.Comment.user_id == user_id).all()


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(limit).all()


def get_comment_by_user_id_ad_id(db: Session, user_id: int, ad_id: int):
    return (
        db.query(models.Comment)
        .filter(models.Comment.user_id == user_id, models.Comment.ad_id == ad_id)
        .all()
    )


def create_comment(db: Session, comment: schemas.CommentCreate):
    db_comment = models.Comment(
        text_value=comment.text_value, user_id=comment.user_id, ad_id=comment.ad_id
    )
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        db.rollback()


def update_comment(db: Session, comment: schemas.Comment, comment_data: dict):
    for field, value in comment_data.items():
        setattr(comment, field, value)
    db.commit()
    return comment


def delete_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return comment
    return None
