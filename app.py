# FastAPI
from fastapi import FastAPI

# DataBase
from db import models
from db.database import engine

# Routes
from routes.users.router import users_router
from routes.tweets.router import tweets_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Twitter API",
    version='1'
)

@app.on_event('startup')
def startup():
    print('The server is starting, welcome')

@app.on_event('shutdown')
def shutdown():
    print('Ending server')

app.include_router(users_router)
app.include_router(tweets_router)