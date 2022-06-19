# Python
from uuid import UUID
from typing import Optional, Union
from datetime import date

# Pydantic
from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password:str = Field(
        ...,
        min_length=8
    )

class User(UserBase):
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
    birth_date: Optional[Union[date, None]] = Field(default=None)

class UserRegister(User):
    password:str = Field(
        ...,
        min_length=8
    )

class UserID(User):
    user_id:str = Field(...)

class UserResponse(User):
    message: Union[str, None]= Field(default=None)
