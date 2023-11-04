from sqlalchemy.orm import Session

from . import models, schemas


def get_ad_by_id(db: Session, ad_id: int):
    return db.query(models.AD).filter(models.AD.id == ad_id).first()

def create_ad(db: Session, ad: schemas.ADCreate):    
    db_ad = models.AD(title=ad.title, description=ad.description, owner_id=ad.owner_id)
    db.add(db_ad)
    db.commit()
    db.refresh(db_ad)
    return db_ad