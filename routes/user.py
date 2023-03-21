from fastapi import APIRouter
from fastapi import status
from config.db import conn
from schemas.user import userEntity, usersentity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId


user=APIRouter()

@user.get(
    path= '/users',
    status_code=status.HTTP_201_CREATED,
    summary= 'Get all user',
    tags= ['Users']    
    )
def find_all_users():
    return usersentity(conn.local.user.find())

@user.post(
    path= '/signup',
    status_code=status.HTTP_201_CREATED,
    summary= 'Regiter an user',
    tags= ['Users']
    )
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]

    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({"_id": id})
    return userEntity(user)

###Login a user
@user.post(
    path= '/login',
    status_code=status.HTTP_200_OK,
    summary= 'login an user',
    tags= ['Users']
    )
def login():
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    pass

@user.get(
    path= '/users/{id}',
    status_code=status.HTTP_201_CREATED,
    summary= 'Get a user by id',
    tags= ['Users']    
    )
def find_user(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.put(
    path= '/users/{id}',
    status_code=status.HTTP_201_CREATED,
    summary= 'Update a user',
    tags= ['Users']
    )
def update_user(id: str, user: User):
    conn.local.user.find_one_and_replace({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.delete(
    path= '/users/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    summary= 'Delete a user',
    tags= ['Users']
    )
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))
    return 'Deleted'