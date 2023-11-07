# login/authentication.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, ExpiredSignatureError, JWTError
from typing import Annotated
from datetime import datetime, timedelta
from decouple import config

from . import schemas, models, crud
from ..database import get_db

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES")

# Define a password hasher
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# This part specifies the URL endpoint where clients can request an OAuth2 access token.
# In this case, it's set to "login," indicating that the access token can be requested
# by clients at the "/login" URL. This URL is typically used for user authentication.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Function to verify user's password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Function to authenticate a user
def authenticate_user(db: Session, user: schemas.UserLogin):
    user_db = db.query(models.User).filter(models.User.username == user.username).first()
    if not user_db:
        return None
    if not verify_password(user.password, user_db.hashed_password):
        return None
    return user_db

def get_current_user( db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        # user_id: str = payload.get("id")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Fetch user data from the database based on the username
        user = crud.get_user_by_username(db, username)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt