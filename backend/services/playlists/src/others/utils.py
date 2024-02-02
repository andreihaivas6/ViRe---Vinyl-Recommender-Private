from flask import current_app
from flask import request

import jwt

class Utils:
    @staticmethod
    def get_token():
        return request.headers.get("Authorization").split(" ")[1]
    
    @staticmethod
    def get_user_id_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["id"]
        except:
            return None
    
    @staticmethod
    def get_user_name_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["username"]
        except:
            return "no-name"
