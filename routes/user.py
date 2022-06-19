# Python 
import json
from typing import Union
from uuid import uuid4

# FastAPI
from fastapi import APIRouter, status
from fastapi import Body, Query, Path

# Models
from models.user import UserLogin, UserResponse, UserRegister

from utils.getdata import get_data

router = APIRouter()

USER_DB = "./db/users.json"

# --------------
# Show all users 
# --------------

@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    tags=["Users"]
)
async def home():
    """
    # This path operation show all tweets in the app

    ## Returns a json list with all tweets in th app, with the following keys

    - tweet_id: UUID
    - content: str
    - created_at: datetime
    - updated_at: Optional[datetime]
    - by: User
    """
    return get_data(USER_DB)

# -----------
#  Get a user 
# -----------
@router.get(
    path="/user",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a User",
    tags=["Users"]
)
async def get_a_user(
    nickname: Union[str, None] = Query(
        None,
        title="Nickname")
    ):
    """
    # Get a User

    ## This path operation get a user 

    ## Parameter:

    - Query parameter: nickname

    ## Return a json with de basic user information

    - user_id: UUID
    - nickname: str
    - first_name: str
    - last_name: str
    - birth_date: str
    - message: str
    """

    db  = get_data(USER_DB,
        path={"nickname": nickname},
        message="This user doesn't exist!")

    user = db["match"]
    user["user_id"] = str(user["user_id"])
    user["birth_date"] = str(user["birth_date"])
    user["message"] = "User exits!"

    return  user

# ----------------
# Signup a account 
# ----------------
@router.post(
    path="/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user",
    tags=["Users"]
)
async def signup(user: UserRegister = Body(...)):
    """
    # Signup

    ## This path operation register a user in the app

    ## Parameters:

    - Request body parameter: 

        - user: UserRegister

    ## Return a json with the basic user information:

    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    data = get_data(USER_DB)
    user_dict = user.dict()
    user_dict["birth_date"] = str(user_dict["birth_date"])
    user_data = {'user_id': str(uuid4())}
    user_data = user_data | user_dict

    data.append(user_data)

    with open(USER_DB, "w", encoding="utf-8") as file:
        file.write(json.dumps(data))

    user_dict["message"] = "User created!"
    
    return user_dict

# ----------------
# Login to account 
# ----------------
@router.post(
    path="/login",
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Login a user",
    tags=["Users"]
)
async def login(user: UserLogin = Body(...)):
    """
    # Log in

    ## This path operation log in to the app

    ## Parameters:

    - Request body parameter: 

        - user: UserRegister

    ## Return a json with the basic user information:

    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    user_dict = user.dict()

    db_users = get_data(
        USER_DB,
        path={"email": user_dict["email"]},
        auth={"password": user_dict["password"]},
        message="This user doesn't exist!")

    user = db_users["match"]
    user["message"] = "Login success!"

    return user

# --------------
# Delete a users 
# --------------
@router.delete(
    path="/delete/{nickname}",
    response_model= UserResponse,
    status_code= status.HTTP_200_OK,
    summary="Delete a user",
    tags=["Users"]
)
async def user_delete(
    nickname: str = Path(
        ...,
        min_length=2,
        max_length=15
    ),
    password: str = Query(
        ...,
        min_length=8
    )
):
    """
    # Delete a User

    ## This path operation delete a user in the app
    
    - Path parameter: nickname
    - Query parameter: user password

    ## Returns a json with the basic information of the deleted user:

    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    db_users = get_data(
        USER_DB,
        path = {"nickname": nickname},
        auth={"password":password},
        message="This user doesn't exist!")

    user = db_users["match"]
    user["message"] = "User Deleted!"

    dict_users = list(filter(lambda x: x["nickname"] != nickname, db_users["data"]))

    with open(USER_DB, "w", encoding="utf-8") as file:
        file.write(json.dumps(dict_users))
    
    return user

# --------------
# Update a users 
# --------------

@router.put(
    path="/update/{nick_name}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="update a user's information",
    tags=["Users"]
)
async def update(
    nick_name:str = Path(...),
    password: str = Query(...),
    new_password: Union[str, None] = Query(None),
    nickname: Union[str, None] = Query(None),
    first_name: Union[str, None] = Query(None),
    last_name: Union[str, None] = Query(None), 
    birth_date: Union[str, None] = Query(None)
):
    """
    # Update a User

    ## This path operation update a user's information in the app

    ## Parameters:
    
    - Path parameter: nickname
    - Query parameter: user password
    - Optional parameters: nickname, first_name, last_name, birth_date, new_password.

    ## Returns a json with the basic information of the deleted user:

    - user_id: UUID
    - email: Emailstr
    - first_name: str
    - last_name: str
    - birth_date: datetime
    """
    query_dict = {
        "nickname": nickname,
        "password": new_password,
        "first_name":first_name,
        "last_name":last_name,
        "birth_date":birth_date
        }

    db_users = get_data(
        USER_DB,
        path={"nickname": nick_name},
        auth={"password":password},
        message="This user doesn't exist!")

    data = db_users["data"]
    user = db_users["match"]

    index_user = list(map(lambda key: 1 if key["nickname"] == nick_name else 0, data)).index(1)

    for k,v in query_dict.items():
            if not query_dict[k] == None:
                data[index_user][k] = v

    user = data[index_user]
    user["message"] = "Updated user"

    with open(USER_DB, "w", encoding="utf-8") as file:
        file.write(json.dumps(data))

    return user