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
            "tracks": [
                {
                    "album": "21",
                    "artist": "Adele",
                    "playlist_id": 1,
                    "title": "Rolling in the Deep",
                    "track_id": 1
                },
                {
                    "album": "21",
                    "artist": "Adele",
                    "playlist_id": 1,
                    "title": "Someone Like You",
                    "track_id": 2
                },
                {
                    "album": "Fearless",
                    "artist": "Taylor Swift",
                    "playlist_id": 1,
                    "title": "You Belong with Me",
                    "track_id": 3
                },
                {
                    "album": "1989",
                    "artist": "Taylor Swift",
                    "playlist_id": 1,
                    "title": "Blank Space",
                    "track_id": 4
                },
                {
                    "album": "Folklore",
                    "artist": "Taylor Swift",
                    "playlist_id": 1,
                    "title": "Cardigan",
                    "track_id": 5
                }
            ],
        }

    except Exception as e:
        return {
            "msg": "Could not get songs"
        }, 400
