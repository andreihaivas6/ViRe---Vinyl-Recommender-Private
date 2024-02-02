# get vinyl data - not needed anymore actually
# get songs data
from flask import Blueprint
from flask import request

from others import auth_middleware, Utils

app_data = Blueprint("app_data", __name__)

# search for songs by name from query params
@app_data.route("/songs", methods=["GET"])
@auth_middleware
def get_songs():
    try:
        song_name = request.args.get("name") # from query params
        if song_name is None:
            return {
                "msg": "Song name is required"
            }, 400
        
        # TODO: get songs from sparql service using song_name
        
        return {
            "msg": "TODO"
        }

    except Exception as e:
        return {
            "msg": "Could not get songs"
        }, 400
