# Python 
import json
from uuid import uuid4
from datetime import datetime

# FastAPI
from fastapi import APIRouter, HTTPException
from fastapi import Body, Path, status

# Models
from models.tweets import TweetResponse, TweetUpdated
from models.user import UserLogin

# utils
from utils.getdata import get_data

router = APIRouter()

TWEETS_DB = "./db/tweets.json"
USER_DB = "./db/users.json"

# ---------------
# Show all tweets 
# ---------------
@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
async def showTweets():
    return get_data(TWEETS_DB)

# ------------
# Show a tweet
# ------------
@router.get(
    path="/{tweet_id}",
    status_code=status.HTTP_200_OK,
    summary="Show a specific tweet",
    response_model=TweetResponse,
    tags=["Tweets"]
)
async def showTweets(tweet_id:str = Path(...)):
    data = get_data(
        TWEETS_DB,
        path={"tweet_id": tweet_id}
        )

    return data["match"]

# ------------
# Post a tweet 
# ------------
@router.post(
    path="/post/{user}",
    response_model=TweetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Post a Tweet",
    tags=["Tweets"]
)
async def post(
    tweet:TweetUpdated = Body(...)
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
    db_tweets = get_data(TWEETS_DB)

    request = tweet.dict()

    email = request['user']['email']
    password = request['user']['password']
    content =  request['content']

    db_users = get_data (
        USER_DB,
        path={"email": email},
        auth={"password": password},
        message="This user doesn't exist!"
    )
    
    user =  db_users["match"]

    ordered_tweet = {'tweet_id': str(uuid4())}
    ordered_tweet["content"] = content
    ordered_tweet["created_at"] = str(datetime.now())
    ordered_tweet["updated_at"] = None
    ordered_tweet['by'] = {
        "user_id": user["user_id"],
        "email": user["email"],        
        "nickname": user["nickname"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "birth_date": user["birth_date"],
    }

    db_tweets.append(ordered_tweet)

    with open(TWEETS_DB, "w", encoding="utf-8") as file:
        file.write(json.dumps(db_tweets))

    ordered_tweet['message'] = "Tweet created!"
    
    return ordered_tweet

# --------------
# Update a tweet 
# --------------
@router.put(
    path="/update/{tweet_id}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
async def update_tweet(
    tweet_id: str = Path(...),
    content: TweetUpdated = Body(...)
    ):
    request_content = content.dict()

    db_tweets = get_data(
        TWEETS_DB,
        path={"tweet_id": tweet_id},
        message="tweet id doesn't exist!"
        )

    tweet = db_tweets["match"]
    tweets = db_tweets["data"]    
    
    db_user = get_data (
         USER_DB,
         path={"email": request_content["user"]["email"]},
         auth={"password": request_content["user"]["password"]},
         message="This user doesn't exist!"
    )

    index_tweet = list(
        map(lambda key: 1 if key["tweet_id"] == tweet_id else 0,
        tweets)
        ).index(1)

    user_email_request = tweet["by"]["email"]
    user_email = db_user["match"]["email"]

    if user_email_request == user_email:
        tweets[index_tweet]["content"] = request_content["content"]
        tweets[index_tweet]["updated_at"] = str(datetime.now())
    else:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="It is not the user corresponding to the tweet"
                )
    
    with open(TWEETS_DB, "w", encoding="utf-8") as file:
        file.write(json.dumps(tweets))
    
    response = tweets[index_tweet]
    response["message"] = "Updated tweet!"
    return response


# --------------
# Delete a tweet 
# --------------
@router.delete(
    path="/delete/{tweet_id}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
async def delete_tweet(
    tweet_id: str = Path(...),
    user: UserLogin = Body(...)
):
    user_request = user.dict()

    db_user = get_data (
         USER_DB,
         path={"email": user_request["email"]},
         auth={"password": user_request["password"]},
         message="This user doesn't exist!"
    )

    if db_user:
            
        db_tweets = get_data(
            TWEETS_DB,
            path={"tweet_id": tweet_id},
            message="tweet id doesn't exist!"
            )
        
        tweets = db_tweets["data"]
        tweet_dict = list(filter(lambda x: x["tweet_id"] != tweet_id, tweets))

        with open(TWEETS_DB, "w", encoding="utf-8") as file:
            file.write(json.dumps(tweet_dict))

        tweet = db_tweets["match"]
        tweet["message"] = "The tweet was deleted!"

        return tweet



