from flask import current_app
from flask import request

import jwt
import json

from pymongo import MongoClient

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
    def get_preferences_for_user(user_id):
        uri = "mongodb+srv://myAtlasDBUser:myAtlasDBUser@myatlasclusteredu.deaxbzf.mongodb.net/?retryWrites=true&w=majority"
        local_uri = "mongodb://localhost:27017/"
        client = MongoClient(local_uri)

        db = client['mydatabase']
        collection = db['preferences_test-6']

        result = collection.find_one({"user_id": user_id})
        print(result)
        return result if result else {}

    @staticmethod
    def make_vinyls_readable(res):
        result = {
            "vinyls": [],
        }
        for elem in res['result']:
            # print(elem)
            if elem["results"]["bindings"]:
                for binding in elem["results"]["bindings"]:
                    vinyl = {}
                    for key, value in binding.items():
                        if key == "genre":
                            genre = value["value"].replace("'", '"')
                            genre = json.loads(genre)
                            genre = ', '.join(genre)
                            vinyl[key] = genre
                        else:
                            vinyl[key] = value["value"]
                    
                    result["vinyls"].append(vinyl)
        return result