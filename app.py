# FastAPI
from fastapi import FastAPI

# Routes
from routes.user import router as user_router
from routes.tweet import router as tweet_router

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

app.include_router(user_router, prefix="/users")
app.include_router(tweet_router, prefix="/tweets")

