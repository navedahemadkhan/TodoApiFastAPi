from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt

SECRET_KEY = "gvghcxgjhvvghv"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password,hash_password):
    return pwd_context.verify(plain_password,hash_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data:dict,expires_delta:timedelta=None):
    to_encode=data.copy()
    if expires_delta:
        expire = datetime.utcnow()+expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None