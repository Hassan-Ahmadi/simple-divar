from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import schemas, crud, exceptions

from ..users.authentication import current_user_dependency

from ..users import crud as users_crud
from ..ads import crud as ads_crud

from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Comment, status_code=201)
async def create_comment(
    comment: schemas.CommentCreate,
    current_user: current_user_dependency,
    db: Session = Depends(get_db),
):
    # validate that user_id exists
    db_user = users_crud.get_user(db=db, user_id=comment.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # validate that ad_id exists
    db_ad = ads_crud.get_ad_by_id(db=db, ad_id=comment.ad_id)
    if db_ad is None:
        raise HTTPException(status_code=404, detail="Ad not found")

    has_comment = crud.get_comment_by_user_id_ad_id(
        db=db, user_id=comment.user_id, ad_id=comment.ad_id
    )
    if has_comment:
        raise exceptions.CommentAlreadyExists()
    else:
        return crud.create_comment(db=db, comment=comment)


@router.get("/", response_model=list[schemas.Comment])
async def get_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_comments(db=db, skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=schemas.Comment)
async def get_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment


# This route accepts a Userupdate schema and returns a User schema
@router.put("/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment_data: schemas.CommentUpdate,
    current_user: current_user_dependency,
    db: Session = Depends(get_db),
):
    db_comment = crud.get_comment_by_id(db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Update user information based on valid parameters using the CRUD function
    updated_comment = crud.update_comment(
        db, db_comment, comment_data.model_dump(exclude_unset=True)
    )

    return updated_comment


@router.delete("/{comment_id}", response_model=schemas.Comment)
async def delete_comment(
    comment_id: int,
    current_user: current_user_dependency,
    db: Session = Depends(get_db),
):
    db_comment = crud.delete_comment(db=db, comment_id=comment_id)
    if db_comment:
        return db_comment
    raise HTTPException(status_code=404, detail="Comment not found")
