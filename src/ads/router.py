from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import schemas, crud
from ..users import crud as users_crud
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.AD, status_code=201)
async def create_ad(ad: schemas.ADCreate, db: Session = Depends(get_db)):
    db_user = users_crud.get_user(db=db, user_id=ad.owner_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_ad(db=db, ad=ad)


@router.get("/{ad_id}", response_model=schemas.AD)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    db_ad = crud.get_ad_by_id(db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return db_ad
