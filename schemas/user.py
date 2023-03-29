def userEntity(user):
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "name": user["name"],
        "email": user["email"],
        "password": user["password"]
    }

def usersentity(users):
    return [userEntity(user) for user in users]