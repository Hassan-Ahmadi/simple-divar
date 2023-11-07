from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

from . import schemas, crud, authentication, models
from ..database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=201)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered!")
    return crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# This route accepts a Userupdate schema and returns a User schema
@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db)
):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Update user information based on valid parameters using the CRUD function
    updated_user = crud.update_user(
        db, db_user, user_data.model_dump(exclude_unset=True)
    )

    return updated_user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    # Authenticate user
    authenticated_user = authentication.authenticate_user(
        form_data.username, form_data.password, db
    )
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create access token
    access_token = authentication.create_access_token(data={"sub": form_data.username})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me/", response_model=schemas.User)
async def read_users_me(
    current_user: Annotated[
        schemas.User, Depends(authentication.get_current_active_user)
    ]
):
    return current_user
