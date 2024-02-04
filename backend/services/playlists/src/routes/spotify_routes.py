from flask import Blueprint
from flask import request
from others import Utils

from repositories import PreferencesRepository
from others import auth_middleware

app_spotify = Blueprint("app_spotify", __name__)

preferences_repository = PreferencesRepository()

@app_spotify.route("/spotify/<string:access_token>", methods=["POST"])
@auth_middleware
def get_spotify_user_info(access_token: str):
    try:
        tracks_response = Utils.get_spotify_user_info(access_token)
        
        preferences_repository.compute_preferences(
            tracks_response, 
            Utils.get_user_id_from_token()
        )

        return tracks_response
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get spotify user info"
        }, 400 
