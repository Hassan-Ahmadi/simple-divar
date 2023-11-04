from fastapi import APIRouter, FastAPI, Request, Response
from dotenv import load_dotenv, find_dotenv

from .users import routes as users_routes

load_dotenv(find_dotenv())

app = FastAPI()

app.include_router(users_routes.router, prefix="/users", tags=["users"])
