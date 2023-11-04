from fastapi import APIRouter, FastAPI, Request, Response
from dotenv import load_dotenv, find_dotenv

from .users import router as users_router
from .ads import router as ads_router

load_dotenv(find_dotenv())

app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(ads_router.router, prefix="/ads", tags=["ads"])
