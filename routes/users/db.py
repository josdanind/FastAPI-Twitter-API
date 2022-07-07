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

# Database Queries
from db.queries import write_row, delete_row, get_all
from db.queries import check_existence

# Schemas
from schemas.user import UserUpdateData
from schemas.user import NicknameUserLogin, EmailUserLogin

# ---------
#  QUERIES
# ---------
# --// GET ALL USERS
def get_all_users(db: Session):
    return get_all(db, model='User')

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

# --// CREATE A USER
def create_user(db: Session, user: UserEntityDB):
    check_existence(
        db,
        model='User',
        error_message="The user exists!",
        nickname = user.nickname,
        error_if_exist=True
    )
    
    user_data = user.dict()
    del user_data['password']
    user_data['hashed_password'] = context.hash(user.password)
    user_data['birth_date'] = str(user_data['birth_date'])

    db_user = write_row(db, 'User', user_data)
    db_user.message = 'User Created!'
     
    return db_user

# --// USER LOGIN
def login_user(
    db: Session,
    login: Union[EmailUserLogin,  NicknameUserLogin]
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
            detail="Invalid password")

# --// DELETE A USER
def delete_user(
    db: Session,
    userLogin: Union[EmailUserLogin,  NicknameUserLogin]
): 
    db_user = login_user(db, userLogin)
    delete_row(db, 'User', id=db_user.id)
    db_user.message = "The user was deleted!"

    return db_user

# --// UPDATE A USER
def update_user(
    db: Session,
    data_user: UserUpdateData
):
    nicknameLogin = data_user.current_credentials
    db_user = login_user(db, nicknameLogin)

    to_update = data_user.credentials_to_update.__dict__

    for k in to_update.keys():
        value = to_update[k]

        if value:
            if k == 'first_name':
                db_user.first_name = value
                continue
            if k == 'email':
                db_user.email = value
                continue 
            if k == 'first_name':
                db_user.first_name = value
                continue
            if k == 'last_name':
                db_user.last_name = value
                continue
            if k == 'birth_date':
                db_user.first_name = value
                continue
            if k == 'password':
                db_user.hashed_password = context.hash(value)
                continue

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_user.message = "The user data was updated!"

    return  db_user