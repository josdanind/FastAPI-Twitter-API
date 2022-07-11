# FastAPI
from fastapi import Depends, Query, status, Body, Path
from fastapi import APIRouter, Response
from fastapi.security import HTTPBasicCredentials


# Models
from schemas.user import UserEntityDB, UserUpdateData
from schemas.user import UserResponse, UserBaseResponse
from schemas.user import EmailUserLogin, NicknameUserLogin

#  Database
from sqlalchemy.orm  import Session
from db.database import SessionLocal
from . import db as users_table

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --------------
# Show all users 
# --------------
@router.get(
    path="",
    response_model =  list[UserBaseResponse],
    status_code=status.HTTP_200_OK
)
async def home(
    db: Session = Depends(get_db),
    page:int = Query(default=0),
    limit:int = Query(default=10)

):
    """
    # Get all users

    This path operation show all users registered in the app

    ## Returns a json with a list of schemas of type: `UserBaseResponse`

    The corresponding scheme shows the basic information of 
    all the users registered in the app.
    """

    return users_table.get_all_users(db, page, limit)

# -----------
#  Get a user 
# -----------
@router.get(
    path="/user/{nickname}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a User"
)
async def get_a_user(
    db: Session = Depends(get_db),
    nickname:str = Path(...)
):
    """
    # Get a User

    This path operation show the specified user.

    ## Required parameters:

    - Path parameter: nickname

    ## Return a json with the model: `UserResponse`

    The corresponding scheme shows the basic user information. 
    """

    return  users_table.get_user(db,  nickname)

# ----------------
# Signup a account 
# ----------------
@router.post(
    path="/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user"
)
async def signup(
    db: Session = Depends(get_db),
    userRequest: UserEntityDB = Body(...)
):
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
   
    return users_table.create_user(db, userRequest)

# ----------------
# Login to account 
# ----------------
@router.post(
    path="/login",
    response_model=UserResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Login a user"
)
async def login(
    db: Session = Depends(get_db),
    emailLogin: EmailUserLogin = Body(...)
):
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

    return users_table.login_user(db, emailLogin)

# --------------
# Delete a users 
# --------------
@router.delete(
    path="/delete/{nickname}",
    response_model= UserResponse,
    status_code= status.HTTP_200_OK,
    summary="Delete a user"
)
async def user_delete(
    db: Session = Depends(get_db),
    nicknameUserLogin: NicknameUserLogin = Body(...)
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

    return users_table.delete_user(db, nicknameUserLogin)

# --------------
# Update a users 
# --------------
@router.put(
    path="/update/{nick_name}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="update a user's information"
)
async def update(
    db: Session = Depends(get_db),
    userRequest: UserUpdateData  = Body(...),
):
    """
    # Update a User
    ## This path operation update a user's information in the app
    ## Parameters:s
    
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

    return users_table.update_user(db, userRequest)