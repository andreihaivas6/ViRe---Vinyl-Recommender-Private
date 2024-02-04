# share playlist with friends
# combine playlist with friends
# import playlist as JSPF

from flask import Blueprint
from flask import request

from others import auth_middleware, Utils
from models import *
from repositories import PlaylistActionsRepository, PreferencesRepository

app_playlist_actions = Blueprint("app_playlist_actions", __name__)

playlist_actions_repository = PlaylistActionsRepository()
preferences_repository = PreferencesRepository()

# share a playlist with a given user_id (playlist must be owned by the current user)
@app_playlist_actions.route("/playlist/share", methods=["POST"])
@auth_middleware
def share_playlist():
    try:
        shared_playlist = shared_playlist_schema.load(request.json)
        result = playlist_actions_repository.share_playlist_id_with_user_id(Utils.get_user_id_from_token(), shared_playlist)

        if result is None:
            return {
                "msg": "Could not share playlist"
            }, 400
        else:
            return shared_playlist_schema.dump(shared_playlist), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not share playlist"
        }, 400


# combine a playlist with another one (both playlists must be owned by the current user) -> resulting in a new playlist with the combined tracks 
@app_playlist_actions.route("/playlist/combine", methods=["POST"])
@auth_middleware
def combine_playlist():
    try:
        first_playlist_id = request.json["first_playlist_id"]
        second_playlist_id = request.json["second_playlist_id"]
        try:
            method = request.json["method"]
        except:
            method = "union"

        result = playlist_actions_repository.combine_playlists(first_playlist_id, second_playlist_id, method)

        if result is None:
            return {
                "msg": "Could not combine playlists"
            }, 400
        else:
            return playlist_schema.dump(result), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not combine playlists"
        }, 400

# import a playlist from a JSPF file
@app_playlist_actions.route("/playlist/import", methods=["POST"])
@auth_middleware
def import_playlist():
    try:
        playlist = request.json["playlist"]
        result = playlist_actions_repository.import_playlist(playlist)

        for track in playlist["track"]:
            track['artist'] = track['creator']
        preferences_repository.compute_preferences(
            playlist["track"], 
            Utils.get_user_id_from_token()
        )

        if result is None:
            return {
                "msg": "Could not import playlist"
            }, 400
        else:
            return playlist_schema.dump(result), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not import playlist"
        }, 400
