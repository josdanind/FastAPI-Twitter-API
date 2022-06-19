# FastAPI
from fastapi import FastAPI

# Routes
from routes.user import router as user_router
from routes.tweet import router as tweet_router

app = FastAPI()

app.include_router(user_router, prefix="/users")
app.include_router(tweet_router, prefix="/tweets")

