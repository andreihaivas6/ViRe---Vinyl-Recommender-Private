from flask import Blueprint
from flask import request
from services.preferences_service import set_user_preferences
from others import auth_middleware, Utils
import requests 
app_recommendation = Blueprint("app_recommendation", __name__)

@app_recommendation.route("/preference", methods=["POST"])
# @auth_middleware
def add_preference():
    text = request.json.get("text", None)
    if not text:
        return {"error": "Missing text"}, 400
    
    queries = set_user_preferences(text)
    print(queries)
    res = requests.post("http://localhost:5003/queries", json={"queries": [queries]}, headers=request.headers).json()
    print(res)

    return {
        "msg": "Preference added"
    }, 201

@app_recommendation.route("/recommend", methods=["GET"])
@auth_middleware
def recommend():
    user_id = Utils.get_user_id_from_token()
    preferences = Utils.get_preferences_for_user(user_id)

    # TODO: Get preferences from nosql database / cache by user_id
    # TODO: Use preferences to call -> Sparql service -> which queries Stardog (from DBpedia) -> returns recommendations

    return {
        "msg": "Recommendations fetched",
        "data": []
    }, 200
