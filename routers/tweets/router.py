# FastAPI
from fastapi import Body, Path, Query, status, Depends
from fastapi import APIRouter

# Auth
from utils.OAuth import oauth2_schema

# Schemas
from schemas.tweets import TweetResponse, TweetBaseResponse
from schemas.tweets import TweetContent

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

router = APIRouter(
    prefix="/tweets",
    tags=["Tweets"]
)

# --// SHOW ALL TWEETS
@router.get(
    path="",
    response_model=list[TweetBaseResponse],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
async def showTweets(
    db: Session = Depends(get_db),
    page:int = Query(default=0),
    limit:int = Query(default=10)
):
    return tweets_table.get_all_tweets(db, page,limit)

# --// SHOW A TWEET
@router.get(
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
@router.post(
    path="/post",
    response_model=TweetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
async def post(
    db: Session = Depends(get_db),
    token:str = Depends(oauth2_schema),
    tweetContent: TweetContent = Body(...),
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
    return tweets_table.post_tweet(db, token, tweetContent)

# --// DELETE A TWEET
@router.delete(
    path="/delete/{tweetId}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
async def delete_tweet(
    db: Session = Depends(get_db),
    tweetId: int = Path(...),
    token:str = Depends(oauth2_schema),
):
    return tweets_table.delete_tweet(db, token, tweetId)

# --// UPDATE A TWEET
@router.put(
    path="/update/{tweet_id}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
async def update_tweet(
    db: Session = Depends(get_db),
    token:str = Depends(oauth2_schema),
    tweet_id: str = Path(...),
    toUpdate: TweetContent = Body(...)
    ):
    
    return tweets_table.update_tweet(db, token, toUpdate, tweet_id)