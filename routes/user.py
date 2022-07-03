# Python 
from typing import Union
from operator import itemgetter

# Externals 
from utils.encrypt import context

# FastAPI
from fastapi import APIRouter, status
from fastapi import Body, Query, Path

# Models
from models.user import UserEntityDB, UserResponse
from models.user import UserLoginEmail, UserUpdateData

#Database
from db.connect_db import connect_db

router = APIRouter()

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
    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    users_data = connect_db.select_all()
    connect_db.on = False
    # // end
    
    for user in users_data:
        del user["password"]
        user["birth_date"] =  str(user["birth_date"])
        user["create_at"] =  str(user["create_at"])

    return users_data
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
    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.existence(
        message="The user does not exist!",
        error_if_exist=False,
        nickname=nickname)
    connect_db.on = False
    # // end
    user_data['birth_date'] = str(user_data['birth_date'])
    user_data['message'] = 'User Exist!'

    return  user_data

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
async def signup(user: UserEntityDB = Body(...)):
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
    
    user_dict = user.dict()
    nickname = user_dict["nickname"]
    user_dict["password"] = context.hash(user_dict["password"])
    
    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    connect_db.existence(message="User exists!", nickname=nickname)
    connect_db.insert_content(user_dict)
    user_data = connect_db.select_row(nickname=nickname)
    connect_db.on = False
    # // end

    user_data['birth_date'] = str(user_data['birth_date'])
    user_data['message'] = 'User Created!'
    return user_data

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
async def login(user: UserLoginEmail = Body(...)):
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

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        email=user_dict["email"],
        password=user_dict["password"]
    )
    connect_db.on = False
    # // end

    return user_data

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

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        nickname=nickname,
        password=password,
    )
    connect_db.delete_row(id=user_data["id"])
    connect_db.on = False
    # // end
    user_data["message"] = "The user was deleted"
    return user_data

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
    userRequest: UserUpdateData  = Body(...),
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

    to_login, to_update = itemgetter(
        "current_credentials",
        "credentials_to_update"
    )(userRequest.dict())

    if to_update["password"]:
        to_update["password"] = context.hash(to_update["password"])

    # database interaction // start
    connect_db.on = True
    connect_db.table = "users"
    user_data = connect_db.login_user(
        nickname=to_login["nickname"],
        password=to_login["password"],
    )
    connect_db.update_row(
        to_update,
        id=user_data["id"])
    user_data = connect_db.select_row(nickname=to_login["nickname"])
    connect_db.on = False
    # // end

    user_data["message"] = "Updated User!"

    return user_data