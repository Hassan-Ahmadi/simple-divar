from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import schemas, crud

from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.ADInDBBase, status_code=201)
async def create_ad(ad: schemas.ADCreate, db: Session = Depends(get_db)):
    return crud.create_ad(db=db, ad=ad)


@router.get("/{ad_id}", response_model=schemas.ADInDBBase)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    db_ad = crud.get_ad_by_id(db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_ad