# Python
from typing import Optional, Union
from datetime import date, datetime

# Pydantic
from pydantic import BaseModel, Field, EmailStr

class UserOrmActive(BaseModel):
    class Config:
        orm_mode = True
class UserEntityDB(BaseModel):
    email: EmailStr
    nickname:str = Field(
        ...,
        min_length=2,
        max_length=15
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[Union[date, None]] = None
    password:str = Field(
        ...,
        min_length=8
    )

class UserBaseResponse(UserOrmActive):
    id:int
    email: EmailStr
    nickname:str = Field(
        ...,
        min_length=2,
        max_length=15
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[Union[date, None]] = None

class UserResponse(UserBaseResponse):
    message: Union[str, None]= None

class EmailUserLogin(UserOrmActive):
    email: EmailStr
    password:str
class UsernameLogin(UserOrmActive):
    nickname:str
    password:str
class UserInformation(BaseModel):
    email: Optional[Union[EmailStr, None]] = None
    nickname: Optional[Union[str, None]] = Field(
        default=None,
        min_length=2,
        max_length=15
    )
    first_name:Optional[Union[str, None]] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    last_name:Optional[Union[str, None]] = Field(
        default=None,
        min_length=1,
        max_length=50
    )
    birth_date:Optional[Union[date, None]] = None
    password:Optional[Union[str, None]] = Field(default=None,min_length=8)

class UserTweets(UserOrmActive):
    id: int
    content: str
    created_at: datetime
    updated_at: Union[datetime, None]