from flask import Blueprint
from flask import request
from others import Utils

app_spotify = Blueprint("app_spotify", __name__)

@app_spotify.route("/spotify/<string:access_token>", methods=["POST"])
def get_spotify_user_info(access_token: str):
    try:
        user_info = Utils.get_spotify_user_info(access_token)
        return user_info
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get spotify user info"
        }, 400 
