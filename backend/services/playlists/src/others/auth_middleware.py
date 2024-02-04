from functools import wraps
from flask import request
from flask import current_app

import jwt

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
            # print(data)
        except jwt.ExpiredSignatureError:
            return {
                "msg": "Token is expired",
                "data": None,
                "error": "Unauthorized"
            }, 401
        except jwt.InvalidTokenError:
            return {
                "msg": "Token is invalid",
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
