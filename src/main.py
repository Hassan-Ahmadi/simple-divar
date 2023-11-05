from fastapi import APIRouter, FastAPI, Request, Response
from dotenv import load_dotenv, find_dotenv

from .users import router as users_router
from .ads import router as ads_router
from .comments import router as comments_router

load_dotenv(find_dotenv())

app = FastAPI(
    title="Simple Divar App",
    description="This fastapi app serves a simple divar app in which users can create ads, and other users can see their ads and leave comments on their ads",
)

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(ads_router.router, prefix="/ads", tags=["ads"])
app.include_router(comments_router.router, prefix="/comments", tags=["comments"])
