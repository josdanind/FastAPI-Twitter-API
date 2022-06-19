from fastapi import HTTPException,status
import json


def get_data(path_db, mode = 'r', path = None, auth = None, message=None):
    data = []
    if path:
        key = list(path.keys()).pop()

    with open(path_db, mode, encoding="utf-8") as file:
        data = json.loads(file.read())
    
    if path and type(key) ==  str:
        match = list(filter(lambda x: x[key] == path[key], data))

        if not match:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )
        
        match = match.pop(0)

        if auth and type(auth) == dict:
            if match["password"] != auth["password"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password"
                )

        return {"data":data, "match": match}

    return data