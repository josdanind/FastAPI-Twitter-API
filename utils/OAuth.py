# Python
from datetime import datetime, timedelta

#JWT
import jwt

# fastAPI
from fastapi.security import OAuth2PasswordBearer

# Environment Variables
from decouple import config
secret_key = config('SECRET_KEY')
algorithm = config('ALGORITHM')
days = int(config('ACCESS_TOKEN_EXPIRE_DAYS'))

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")

def create_access_token(User, days=days):
    data = {
        'user_id': User.id,
        'username': User.nickname,
        'exp': datetime.utcnow() + timedelta(days=days)
    }

    return jwt.encode(data, secret_key, algorithm=algorithm)

def decode_access_token(token):
    try:
        return jwt.decode(token, secret_key, algorithms=[algorithm])
    except Exception as err:
        return None