from datetime import datetime, timedelta
from fastapi import APIRouter
from fastapi import status, HTTPException ,Depends
from config.db import conn
from core import security
from schemas.user import userEntity, usersentity
from models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId


user=APIRouter()

@user.get(
    path= '/users',
    status_code=status.HTTP_200_OK,
    summary= 'Get all user',
    tags= ['Users']    
    )
def find_all_users():
    return usersentity(conn.user.find())

@user.get(
    path= '/users/username',
    status_code=status.HTTP_200_OK,
    summary= 'Get a user by username',
    tags= ['Users']    
    )
def find_a_users_by_username(username: str):
    user = conn.user.find_one({"username":username})
    return userEntity(user)

@user.post(
    path= '/signup',
    status_code=status.HTTP_201_CREATED,
    summary= 'Regiter an user',
    tags= ['Users']
    )
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = security.get_password_hash(new_user["password"])
    del new_user["id"]

    id = conn.user.insert_one(new_user).inserted_id
    user = conn.user.find_one({"_id": id})
    return userEntity(user)

###Login a user
@user.post(
    path= '/login',
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
    )
def login(        
        form_data:OAuth2PasswordRequestForm = Depends()
        ):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = security.authenticate(
        username=form_data.username, password=form_data.password
        )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username")
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
        user["id"], expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        }

@user.get(
    path= '/users/{id}',
    status_code=status.HTTP_201_CREATED,
    summary= 'Get a user by id',
    tags= ['Users']    
    )
def find_user(id: str):
    return userEntity(conn.user.find_one({"_id": ObjectId(id)}))

@user.put(
    path= '/users/{id}',
    status_code=status.HTTP_201_CREATED,
    summary= 'Update a user',
    tags= ['Users']
    )
def update_user(id: str, user: User):
    conn.local.user.find_one_and_replace({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.user.find_one({"_id": ObjectId(id)}))

@user.delete(
    path= '/users/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete a user',
    tags= ['Users']
    )
def delete_user(id: str):
    userEntity(conn.user.find_one_and_delete({"_id":ObjectId(id)}))
    return 'Deleted'