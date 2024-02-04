from flask import Blueprint
from flask import request
from services.preferences_service import get_input_from_text
from services.query_builder import sparql_query_builder_for_preferences
from others import auth_middleware, Utils

app_recommendation = Blueprint("app_recommendation", __name__)

@app_recommendation.route("/preference", methods=["POST"])
# @auth_middleware
def add_preference():
    text = request.json.get("text", None)
    if not text:
        return {"error": "Missing text"}, 400
    
    sentences = text.split('. ')
    query = ""
    for sentence in sentences:
        my_preferences = get_input_from_text(sentence)
        query += sparql_query_builder_for_preferences(my_preferences) + "\n\n\n"
 
    return {
        "msg": "Preference added"
    }, 201

@app_recommendation.route("/recommend", methods=["GET"])
@auth_middleware
def recommend():
    user_id = Utils.get_user_id_from_token()

    # TODO: Get preferences from nosql database / cache by user_id
    # TODO: Use preferences to call -> Sparql service -> which queries Stardog (from DBpedia) -> returns recommendations

    return {
        "msg": "Recommendations fetched",
        "data": []
    }, 200