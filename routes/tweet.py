# Python 
from datetime import datetime
from operator import itemgetter

# FastAPI
from fastapi import APIRouter, HTTPException
from fastapi import Body, Path, status

# Models
from models.tweets import TweetEntityDB, TweetResponse
from models.user import UserLoginNickname

# Database
from db.connect_db import connect_db

router = APIRouter()

def tweet_response(tweet_data, user_data, message=None):

    return {
        "id": tweet_data["id"],
        "content": tweet_data["content"],
        "created_at": str(tweet_data["created_at"]),
        "updated_at": tweet_data["updated_at"],
        "by": user_data,
        "message": message
    }

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
    user_fields = "users.id, email, nickname, first_name, last_name, birth_date"
    tweets_fields = "tweets.id, content, created_at, updated_at"
    fields = user_fields + ", " + tweets_fields
    table_1 = "users"
    table_2 = "tweets"

    query = (
        f"SELECT {fields} "
        f"FROM {table_1} INNER JOIN {table_2} "
        f"ON {table_1}.id={table_2}.user_id;"
    )

    # database interaction // start
    connect_db.on = True
    connect_db.cursor.execute(query)
    data = connect_db.cursor.fetchall()
    column_names = [head[0] for head in connect_db.cursor.description]
    connect_db.on = False
    # // end

    user_head = column_names[:6]
    tweets_head = column_names[6:]

    response = []

    for tweet in data:
        user_dict = dict(zip(user_head, tweet[0:6]))
        tweet_dict = dict(zip(tweets_head, tweet[6:]))
        dict_data = tweet_response(tweet_dict, user_dict)
        del dict_data["message"]
        response.append(dict_data)

    return response

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
    # database interaction // start
    connect_db.on = True
    connect_db.table = "tweets"
    tweet_data = connect_db.existence(
        id=tweet_id,
        message="Tweet don't exist!",
        error_if_exist=False)
    connect_db.table = "users"
    user_data = connect_db.select_row(id=tweet_data["user_id"])
    connect_db.on = False
    # // end

    return tweet_response(
        tweet_data,
        user_data,
        message="Tweet exist!")

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
    userLogin: UserLoginNickname = Body(...),
    tweet:TweetEntityDB = Body(...)
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

    nickname, password = itemgetter(
        "nickname",
        "password"
    )(userLogin.dict())

    content = tweet.dict()["content"]

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        nickname=nickname,
        password=password
    )
    tweet_fields = {
        "user_id": user_data['id'],
        "content": content,
        "created_at": datetime.now()
    }
    connect_db.table = "tweets"
    connect_db.insert_content(tweet_fields)
    tweet_data = connect_db.select_row(
        created_at=tweet_fields["created_at"])
    connect_db.on = False
    # // end

    return tweet_response(
        tweet_data,
        user_data,
        message="Posted tweet!")


# --------------
# Update a tweet 
# --------------
@router.put(
    path="/update/{tweetId}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
async def update_tweet(
    tweetId: str = Path(...),
    userLogin: UserLoginNickname = Body(...),
    toUpdate: TweetEntityDB = Body(...)
    ):
    nickname, password = itemgetter(
        "nickname",
        "password"
    )(userLogin.dict())

    request_content = toUpdate.dict()

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        nickname=nickname,
        password=password
    )
    connect_db.table = "tweets"
    data_tweet = connect_db.existence(
        message=f"Tweet with id={tweetId} don't exist!",
        error_if_exist=False,
        id=tweetId
    )
    if data_tweet["user_id"] == user_data["id"]:
        connect_db.update_row(
            {
                "content": request_content["content"],
                "updated_at": datetime.now()
            },
            id=tweetId
        )
        data_tweet = connect_db.select_row(id=tweetId)
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This tweet isn't yours!s")
    connect_db.on = False
    # // end

    response = tweet_response(
        data_tweet,
        user_data,
        message="The tweet was updated")

    return response

# --------------
# Delete a tweet 
# --------------
@router.delete(
    path="/delete/{tweetId}",
    response_model=TweetResponse,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
async def delete_tweet(
    tweetId: str = Path(...),
    userLogin: UserLoginNickname = Body(...),

):
    nickname, password = itemgetter(
        "nickname",
        "password"
    )(userLogin.dict())

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        nickname=nickname,
        password=password
    )
    connect_db.table = "tweets"
    data_tweet = connect_db.existence(
        message=f"Tweet with id={tweetId} don't exist!",
        error_if_exist=False,
        id=tweetId
    )
    if data_tweet["user_id"] == user_data["id"]:
        connect_db.delete_row(id=tweetId)
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This tweet isn't yours!s")
    connect_db.on = False
    # // end

    response = tweet_response(
        data_tweet,
        user_data,
        message="The tweet was deleted!")

    return response



