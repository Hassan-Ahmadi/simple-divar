from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import schemas, crud
from ..users import crud as users_crud

from ..users.authentication import current_user_dependency
from typing import Annotated

from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.AD, status_code=201)
async def create_ad(
    ad: schemas.ADCreate,
    current_user: current_user_dependency,
    db: Session = Depends(get_db),
):
    db_user = users_crud.get_user(db=db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_ad(db=db, ad=ad, owner_id=current_user.id)


@router.get("/", response_model=list[schemas.AD])
async def get_ads(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_ads(db=db, skip=skip, limit=limit)


@router.get("/{ad_id}", response_model=schemas.AD)
async def get_ad(ad_id: int, db: Session = Depends(get_db)):
    db_ad = crud.get_ad_by_id(db, ad_id=ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")
    return db_ad


@router.put("/{ad_id}", response_model=schemas.AD, status_code=200)
async def update_ad(
    ad_id: int,
    ad_data: schemas.ADUpdate,
    current_user: current_user_dependency,
    db: Session = Depends(get_db),
):
    db_ad = crud.get_ad_by_id(db=db, ad_id=ad_id)
    if db_ad:
        updated_ad = crud.update_ad(
            db=db, ad=db_ad, ad_data=ad_data.model_dump(exclude_unset=True)
        )
        return updated_ad
    raise HTTPException(status_code=404, detail="Ad not found")


@router.delete("/{ad_id}", response_model=schemas.AD)
async def delete_ad(
    ad_id: int,
    current_user: current_user_dependency,
    db: Session = Depends(get_db)
):
    db_ad = crud.delete_ad(db=db, ad_id=ad_id)
    if db_ad:
        return db_ad
    raise HTTPException(status_code=404, detail="Ad not found")
