from flask import Blueprint
from flask import request
from others import discog_api

from others import auth_middleware, Utils
from repositories import PreferencesRepository

preferences_repository = PreferencesRepository()

app_discog = Blueprint("app_discog", __name__)

@app_discog.route("/discog", methods=["GET"])
def get_discog_user_info():
    try:
        user_token_request = discog_api.get_token()
        return user_token_request
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog user info"
        }, 400


@app_discog.route("/discog/verifier", methods=["POST"])
@auth_middleware
def post_discog_verifier():
    verifier = request.json.get("verifier")
    try:
        tracks_response = discog_api.set_verifier(verifier)
        
        preferences_repository.compute_preferences(
            tracks_response, 
            Utils.get_user_id_from_token()
        )

        return tracks_response
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get discog user info"
        }, 400

