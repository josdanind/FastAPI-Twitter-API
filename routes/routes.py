from fastapi import APIRouter

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

tweets_router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)