from functools import wraps
from flask import request
from flask import current_app

import jwt

from repositories import UserRepository

def auth_middleware(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return {
                "msg": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        
        try:
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            print(data)
            current_user = UserRepository().get_user_by_id(data["id"])

            if current_user is None or not current_user.is_active:
                return {
                    "msg": "Invalid Authentication token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except Exception as e:
            return {
                "msg": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 401

        return f(*args, **kwargs)

    return decorated
