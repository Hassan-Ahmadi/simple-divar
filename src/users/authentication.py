# login/authentication.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, ExpiredSignatureError, JWTError

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
    user_db = db.query(models.User).filter(models.User.email == user.email).first()
    if not user_db:
        return None
    if not verify_password(user.password, user_db.password):
        return None
    return user_db


def extract_user_id_from_token(token):
    try:
        # Decode and verify the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # Extract the user ID from the token (assuming it's stored as 'sub')
        user_id = payload.get("sub")

        return user_id

    # Handle token expiration error
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")

    except JWTError as e:
        raise HTTPException(
            status_code=401, detail="Token verification failed: " + str(e)
        )


def get_user_by_token(token: str, db: Session):
    # Implement token verification logic here
    # This can involve decoding a JWT, validating an OAuth2 token, etc.

    # If the token is valid, extract user identification information
    user_id = extract_user_id_from_token(token)

    # Query the database to fetch the user based on the extracted ID
    user = db.query(models.User).filter(models.User.id == user_id).first()

    return user


# def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
#     user = get_user_by_token(token, db)
#     if user is None:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return user

def get_current_user( db: Session, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # token_data = db.query(models.User).filter(models.User.email==email).first()
        # token_data = schemas.User(email=email)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return crud.get_user_by_email(db, email)

def get_current_active_user(db: Session, token: str = Depends(oauth2_scheme)):
    user = get_user_by_token(token, db)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    else:
        if not user.is_active:
            raise HTTPException(status_code=403, detail="Inactive user")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt