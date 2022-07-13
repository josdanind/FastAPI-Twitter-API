# Python
from typing import Union

# SQLAlchemy
from sqlalchemy.orm  import Session

#  FatsAPI
from fastapi import HTTPException, status

# Schemas
from schemas.user import UserEntityDB

# Encrypt password
from utils.encrypt import context

# OAuth
from utils.OAuth import decode_access_token

# Database Queries
from db.queries import write_row, delete_row, get_all
from db.queries import check_existence

# Schemas
from schemas.user import UserInformation
from schemas.user import UsernameLogin, EmailUserLogin
from schemas.jwt import Token

# -------
#  UTILS
# -------
def validate_user(db:Session,token:Token):
    jwt_data = decode_access_token(token)

    if jwt_data:
        return check_existence(
            db,
            'User',
            error_message="User don't  Exists!",
            id=jwt_data["user_id"]
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access Token invalid!",
            headers={'WWW-Authenticate': 'Bearer'}
            )
# ---------
#  QUERIES
# ---------
# --// GET ALL USERS
def get_all_users(
    db:Session,
    page:int = 0,
    limit:int = 5
):
    return get_all(
        db,
        model='User',
        skip=page,
        limit=limit
    )

# --// GET A USER
def get_user(db: Session, nickname: str):
    db_user = check_existence(
        db,
        model='User',
        error_message="The user don't exists!",
        nickname=nickname,
    )
    db_user.message = "The user exists!"

    return db_user

# --// USER LOGIN
def login_user(
    db: Session,
    login: Union[EmailUserLogin,  UsernameLogin]
):
    email_login = (type(login).__name__ == 'EmailUserLogin')
    key = 'email' if email_login else 'nickname'
    value = login.email if email_login else login.nickname

    db_user = check_existence(
        db,
        model ='User',
        error_message = "User don't exist!",
        **{f"{key}": value}
    )

    if context.verify(login.password, db_user.hashed_password):
        db_user.message = 'Login success!'
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

# --// DELETE A USER
def delete_user(
    db: Session,
    token: Token
): 
    db_user = validate_user(db, token)
    delete_row(db, 'User', id=db_user.id)
    db_user.message = "The user was deleted!"

    return db_user

# --// CREATE A USER
def create_user(db: Session, user: UserEntityDB):

    conditions = [
        ("nickname", "The user exists!"),
        ("email", "There is a user with that email!")   
    ]

    for field, message in conditions:
        check_existence(
            db,
            model='User',
            error_message=message,
            error_if_exist=True,
            **{f"{field}": eval(f"user.{field}")}
        )

    user_data = user.dict()
    user_data['hashed_password'] = user_data.pop('password')
    user_data['birth_date'] = str(user_data['birth_date'])

    db_user = write_row(db, 'User', with_dict= user_data)
    db_user.message = 'User Created!'
    
    return db_user

# --// UPDATE A USER
def update_user(
    db: Session,
    token: Token,
    toUpdate: UserInformation
):
    db_user = validate_user(db, token)
    to_update = toUpdate.__dict__
     
    for k in to_update.keys():
        value = to_update[k]

        if value and k != "password":
            exec(f"db_user.{k} = '{value}'")

        if value and k == "password":
            db_user.set_password(value)

    db_user = write_row(db,'User',withModel=db_user)
    db_user.message = "The user data was updated!"

    return  db_user

# --// Get all user's tweets
def user_tweets(
    db: Session,
    token: Token
):
    return validate_user(db, token).tweets