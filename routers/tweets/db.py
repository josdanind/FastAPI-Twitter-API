# Python
from datetime import datetime

# fastAPI
from fastapi import HTTPException, status

# SQLAlchemy
from sqlalchemy.orm  import Session

# Schemas
from schemas.tweets import TweetUserRequest, TweetResponse
from schemas.user import NicknameUserLogin

# Basic queries
from db.queries import write_row, get_all, delete_row
from db.queries import check_existence

# users table queries
from ..users.db import login_user

# --// Response model
def tweet_response(db_user, db_tweet, message=None):
    return  TweetResponse(
        id = db_tweet.id,
        content = db_tweet.content,
        created_at = db_tweet.created_at,
        updated_at = db_tweet.updated_at,
        by = db_user,
        message = message
    )
    
# ---------
#  TWEETS QUERIES
# ---------
# --// POST TWEET
def post_tweet(db:Session, tweet: TweetUserRequest):
    db_user = login_user(db, tweet.user_login)
    tweet_model = {
        "user_id": db_user.id,
        "content": tweet.tweet_details.content,
    }
    db_tweet = write_row(db, 'Tweet', with_dict=tweet_model)

    return tweet_response(
        db_user,
        db_tweet,
        message='Tweet Created!'
    )

# --// GET TWEET
def get_tweet(db: Session, **condition):
    db_tweet =  check_existence(
        db,
        'Tweet',
        error_message="Tweet don't exists",
        **condition
    )
    db_user = db_tweet.user

    return tweet_response(
        db_user,
        db_tweet,
        message='The tweet Exists!'
    )

# --// GET ALL TWEETS
def get_all_tweets(
    db:Session,
    page:int = 0,
    limit:int = 5
):
    db_tweets = get_all(
        db,
        model='Tweet',
        skip=page,
        limit=limit
)
    response = []

    for tweet in db_tweets:
        db_user = tweet.user
        model = {
            "id": tweet.id,
            "content": tweet.content,
            "created_at": tweet.created_at,
            "updated_at": tweet.updated_at,
            "by": db_user,
        }
        response.append(model)

    return response
        
# --// DELETE TWEET
def delete_tweet(
    db:Session,
    login:NicknameUserLogin,
    tweet_id:int
):
    db_user = login_user(db, login)
    db_tweet =  check_existence(
        db,
        'Tweet',
        error_message = "Tweet don't exists",
        id = tweet_id
    )
    delete_row(db, 'Tweet', id=tweet_id)
    
    return tweet_response(
        db_user,
        db_tweet,
        message='The tweet was deleted!'
    )

# --// UPDATE TWEET
def update_tweet(
    db:Session,
    userRequest: TweetUserRequest,
    tweet_id: int
):
    db_user = login_user(db, userRequest.user_login)
    db_tweet = check_existence(
        db,
        'Tweet',
        error_message="Tweet don't exists",
        id = tweet_id
    )
    content =  userRequest.tweet_details.content

    if db_tweet.user_id == db_user.id:
        db_tweet.content =  content
        db_tweet.updated_at = datetime.now()
    else:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="The tweet isn't  yours"
        )
    
    db.add(db_tweet)
    db.commit()
    db.refresh(db_tweet)

    return tweet_response(
        db_user,
        db_tweet,
        message='The tweet was updated!'
    )