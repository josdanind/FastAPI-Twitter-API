# FastAPI
from fastapi import Body, Path, status, Depends
from routes.routes import tweets_router

# Schemas
from schemas.tweets import TweetResponse, TweetBaseResponse
from schemas.tweets import TweetUserRequest
from schemas.user import NicknameUserLogin

# Database
from sqlalchemy.orm import Session
from . import db as tweets_table
from db.database import SessionLocal

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --// SHOW ALL TWEETS
@tweets_router.get(
    path="",
    response_model=list[TweetBaseResponse],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
async def showTweets(db: Session = Depends(get_db),):
    return tweets_table.get_all_tweets(db)

# --// SHOW A TWEET
@tweets_router.get(
    path="/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Show a specific tweet",
    response_model= TweetResponse,
    tags=["Tweets"]
)
async def showTweet(
    db: Session = Depends(get_db),
    tweet_id:int = Path(...)
):

    return tweets_table.get_tweet(db, id=tweet_id)

# --// POST A TWEET
@tweets_router.post(
    path="/post/{user}",
    response_model=TweetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
async def post(
    db: Session = Depends(get_db),
    userRequest: TweetUserRequest = Body(...),
    ):
    """
    # Post a Tweet

    ## This path operation post a tweet in the app

    ## Parameter

    - Request body: Tweet model
    - Path parameter: nickname
    - Query parameter: user's password

    ## return a json with de basic tweet an user information: TweetResponse model
    """
    return tweets_table.post_tweet(db, userRequest)

# --// DELETE A TWEET
@tweets_router.delete(
    path="/delete/{tweetId}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
async def delete_tweet(
    db: Session = Depends(get_db),
    tweetId: int = Path(...),
    userLogin: NicknameUserLogin = Body(...),

):
    return tweets_table.delete_tweet(db, userLogin, tweetId)

# --// UPDATE A TWEET
@tweets_router.put(
    path="/update/{tweet_id}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
async def update_tweet(
    db: Session = Depends(get_db),
    tweet_id: str = Path(...),
    userRequest: TweetUserRequest = Body(...),
    ):
    # database interaction // start
    return tweets_table.update_tweet(db, userRequest, tweet_id)
    # // end