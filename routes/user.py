from fastapi import APIRouter
from config.db import conn
from schemas.user import userEntity, usersentity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId


user=APIRouter()

@user.get('/users')
def find_all_users():
    return usersentity(conn.local.user.find())

@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]

    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({"_id": id})
    return userEntity(user)

@user.get('/users/{id}')
def find_user(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.put('/users/{id}')
def update_user(id: str, user: User):
    conn.local.user.find_one_and_replace({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))

@user.delete('/users/{id}')
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id":ObjectId(id)}))
    return 'Deleted'