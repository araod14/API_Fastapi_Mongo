def userEntity(item):
    return {
        "id": str(item["_id"]),
        "username": item["username"],
        "name": item["name"],
        "email": item["email"],
        "password": item["password"]
    }

def usersentity(entity):
    return [userEntity(item) for item in entity]