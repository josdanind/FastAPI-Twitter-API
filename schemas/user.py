# Python
from typing import Optional, Union
from datetime import date

# Pydantic
from pydantic import BaseModel, Field, EmailStr

class UserEntityDB(BaseModel):
    email: EmailStr = Field(...)
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
    password:str = Field(
        ...,
        min_length=8
    )

class UserBaseResponse(BaseModel):
    id:int = Field(...)
    email: EmailStr = Field(...)
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

    class Config:
        orm_mode = True

class UserResponse(UserBaseResponse):
    message: Union[str, None]= Field(default=None)
    
    class Config:
        orm_mode = True

class EmailUserLogin(BaseModel):
    email: EmailStr = Field(...)
    password:str = Field(...)

    class Config:
        orm_mode = True

class NicknameUserLogin(BaseModel):
    nickname:str = Field(...)
    password:str = Field(...)

    class Config:
        orm_mode = True

class UserInformationUpdate(BaseModel):
    email: Optional[Union[EmailStr, None]] = Field(default=None)
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
    birth_date:Optional[Union[date, None]] = Field(default=None)
    password:str = Field(default=None,min_length=8)

class UserUpdateData(BaseModel):
    current_credentials: NicknameUserLogin = Field(...)
    credentials_to_update: UserInformationUpdate