# share playlist with friends
# combine playlist with friends
# import playlist as JSPF

from flask import Blueprint
from flask import request

from others import auth_middleware, Utils
from models import *
from repositories import PlaylistActionsRepository

app_playlist_actions = Blueprint("app_playlist_actions", __name__)

playlist_actions_repository = PlaylistActionsRepository()

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


# combine a playlist with 