# FastAPI
from fastapi import FastAPI, APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

# DataBase
from db import models
from db.database import engine

# Routes
from routers import users_router
from routers import tweets_router

# Environment Variables
from decouple import config
version = config('VERSION')

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Twitter API",
    version='1'
)

api = APIRouter(prefix=f'/api/v{version}')
api.include_router(users_router)
api.include_router(tweets_router)

app.include_router(api)

@app.on_event('startup')
def startup():
    print('The server is starting, welcome')

@app.on_event('shutdown')
def shutdown():
    print('Ending server')