from sqlalchemy.orm import Session

from . import models, schemas


def get_ads(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AD).offset(skip).limit(limit).all()

def get_ad_by_id(db: Session, ad_id: int):
    return db.query(models.AD).filter(models.AD.id == ad_id).first()

def create_ad(db: Session, ad: schemas.ADCreate, owner_id: int):    
    db_ad = models.AD(title=ad.title, description=ad.description, owner_id=owner_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad

def update_ad(db: Session, ad: models.AD, ad_data: dict):
    for field, value in ad_data.items():
        setattr(ad, field, value)
    db.commit()
    return ad

def delete_ad(db: Session, ad_id: int):
    db_ad = db.query(models.AD).filter(models.AD.id == ad_id).first()
    if db_ad:
        db.delete(db_ad)
        db.commit()
        return db_ad
    return None