# Python
from typing import Union
from datetime import datetime

# Pydantic
from pydantic import BaseModel, Field

# Models
from schemas.user import UserBaseResponse, NicknameUserLogin

# Tweets Model
class TweetBase(BaseModel):
    content: str= Field(...)

class TweetUserRequest(BaseModel):
    user_login:NicknameUserLogin
    tweet_details:TweetBase

class TweetBaseResponse(BaseModel):
    id: int  = Field(...)
    content: str = Field(...)
    created_at: datetime = Field(...)
    updated_at: Union[datetime, None] = Field(default=None)
    by: UserBaseResponse = Field(...)

class TweetResponse(TweetBaseResponse):
    message: Union[str, None] = Field(default=None)