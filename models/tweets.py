# Python
from uuid import UUID
from typing import Union

# Pydantic
from pydantic import BaseModel, Field

# Models
from models.user import UserID, UserLogin

# Tweets Model
class Tweet(BaseModel):
    content:str = Field(
        ...,
        min_length=1,
        max_length=256
    )

class TweetUpdated(Tweet):
    user: UserLogin = Field(...)

class TweetResponse(Tweet):
    tweet_id: UUID = Field(...)
    by: UserID = Field(...)
    message: Union[str, None]= Field(default=None)
