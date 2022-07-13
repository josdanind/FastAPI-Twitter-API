# Python
from typing import Union
from datetime import datetime

# Pydantic
from pydantic import BaseModel

# Models
from schemas.user import UserBaseResponse

# Tweets Model
class TweetContent(BaseModel):
    content: str
    
class TweetBaseResponse(BaseModel):
    id: int 
    content: str
    created_at: datetime
    updated_at: Union[datetime, None] = None
    by: UserBaseResponse

class TweetResponse(TweetBaseResponse):
    message: Union[str, None] = None