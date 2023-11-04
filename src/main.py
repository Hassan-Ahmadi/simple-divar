from fastapi import APIRouter, FastAPI, Request, Response
from dotenv import load_dotenv, find_dotenv

from .users import router as users_router

load_dotenv(find_dotenv())

app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["users"])
