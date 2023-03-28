from schemas.user import userEntity, usersentity
from config.db import conn
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from bson import ObjectId


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = "e3f21f5576fef93b5c2ecb09183860caec7b46966f0777b6533f0cb92c39baa4"
# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES = 60

##Create token acces
def create_access_token(
    subject: Union[str, Any], 
    expires_delta: timedelta = None
    ) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes = ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def get_user_by_username(username: str): 
    return userEntity(conn.local.user.find_one({"username": ObjectId(username)}))

def authenticate(*, username: str, password: str):
    user = get_user_by_username(username=username)
    if not user:
        return None
    #password_db = db.query(Users).filter(Users.password==password)
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="wrong password")
    return user

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = get_user_by_username(username=token)
    if not user:
        raise HTTPException(
            status_code=400, 
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user