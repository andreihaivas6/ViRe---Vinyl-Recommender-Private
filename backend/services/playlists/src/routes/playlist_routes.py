# playlist get, get all, create, update
# get shared playlists
from flask import Blueprint
from flask import request

from typing import List, Dict

import requests

from others import auth_middleware, Utils
from repositories import PlaylistRepository
from models import *

app_playlist = Blueprint("app_playlist", __name__)

playlist_repository = PlaylistRepository()

# get playlist by id
@app_playlist.route("/playlist/<int:playlist_id>", methods=["GET"])
@auth_middleware
def get_playlist_by_id(playlist_id: int):
    try:
        playlist = playlist_repository.get_playlist_by_id(playlist_id)
        if playlist is None:
            return {
                "msg": "Playlist not found"
            }, 404

        if not playlist.imported_from_jspf:
            track_ids = playlist.track_ids
            ids_build = Utils.build_song_ids(track_ids)
            query = """
                SELECT ?songURI ?title ?genre ?duration ?date
                    WHERE {
                    VALUES ?songURI {""" + ids_build + """}

                    ?songURI a ns1:Song ;
                                dc:title ?title ;
                                dc:date ?date ;
                                ns1:duration ?duration ;
                                ns1:genre ?genre .
                    }
                """
            
            res = requests.post("http://localhost:5003/query", json={"query": query})
            # TODO: get tracks from sparql service using track_ids and append it to playlist for return
            """add field "tracks": [ {}, 
                    {
                        "title": "title",
                        "artist": "artist",
                        "album": "album",
                        "duration": "duration",
                        "genre": "genre",
                        "date": "date"
                    }, ...] 
                """
            return playlist.to_json()
        
        else:
            return playlist_repository.add_track_to_jspf_playlist(playlist)
            
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get playlist"
        }, 400

# get playlists of user id (from token)
@app_playlist.route("/playlist", methods=["GET"])
@auth_middleware
def get_playlists_of_user_id():
    try:
        user_id = Utils.get_user_id_from_token()
        playlists = playlist_repository.get_playlists_of_user_id(user_id)

        shared_playlists = playlist_repository.get_playlists_shared_with_username(Utils.get_user_name_from_token())
        playlists.extend(shared_playlists)

        playlists_to_return = list()
        for playlist in playlists:
            if not playlist.imported_from_jspf:
                track_ids = playlist.track_ids
                # tracks_ids should looks like this: ['songname1', 'songname2', ...]
                ids_build = Utils.build_song_ids(track_ids)
                query = """
                    SELECT ?songURI ?title ?genre ?duration ?date
                        WHERE {
                        VALUES ?songURI {""" + ids_build + """}

                        ?songURI a ns1:Song ;
                                    dc:title ?title ;
                                    dc:date ?date ;
                                    ns1:duration ?duration ;
                                    ns1:genre ?genre .
                        }
                    """
                
                res = requests.post("http://localhost:5003/query", json={"query": query})

                # TODO: get tracks from sparql service using track_ids and append it to playlist for return
                """add field "tracks": [ {}, 
                    {
                        "title": "title",
                        "artist": "artist",
                        "album": "album",
                        "duration": "duration",
                        "genre": "genre",
                        "date": "date"
                    }, ...] 
                """

                playlists_to_return.append(playlist.to_json())
            else:
                playlists_to_return.append(
                    playlist_repository.add_track_to_jspf_playlist(playlist)
                )

        return playlists_to_return
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get playlists"
        }, 400

# get playlists for a given user_id (from path) - /playlist/user/<int:user_id>
@app_playlist.route("/playlist/user/<int:user_id>", methods=["GET"])
@auth_middleware
def get_playlists_of_user_id_path(user_id: int):
    try:
        playlists = playlist_repository.get_playlists_of_user_id(user_id)

        playlists_to_return = list()
        for playlist in playlists:
            if not playlist.imported_from_jspf:
                track_ids = playlist.track_ids

                # TODO: get tracks from sparql service using track_ids and append it to playlist for return
                """add field "tracks": [ {}, 
                    {
                        "title": "title",
                        "artist": "artist",
                        "album": "album",
                        "duration": "duration",
                        "genre": "genre",
                        "date": "date"
                    }, ...] 
                """

                playlists_to_return.append(playlist.to_json())
            else:
                playlists_to_return.append(
                    playlist_repository.add_track_to_jspf_playlist(playlist)
                )

        return playlists_to_return
    except Exception as e:
        print(e)
        return {
            "msg": "Could not get playlists"
        }, 400
        

# create playlist
@app_playlist.route("/playlist", methods=["POST"])
@auth_middleware
def create_playlist():
    try:
        playlist = playlist_schema.load(request.json)
        playlist.user_id = Utils.get_user_id_from_token()
        playlist.user_name = Utils.get_user_name_from_token()
        created_playlist = playlist_repository.create_playlist(playlist)
        
        if created_playlist is None:
            return {
                "msg": "Could not create playlist"
            }, 400
        else:
            return playlist_schema.dump(created_playlist), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not create playlist"
        }, 400

# delete playlist
@app_playlist.route("/playlist/<int:playlist_id>", methods=["DELETE"])
@auth_middleware
def delete_playlist(playlist_id: int):
    try:
        deleted_playlist = playlist_repository.delete_playlist(playlist_id)
        if deleted_playlist is None:
            return {
                "msg": "Could not delete playlist"
            }, 400
        else:
            return playlist_schema.dump(deleted_playlist)
    except Exception as e:
        print(e)
        return {
            "msg": "Could not delete playlist"
        }, 400

# add track to playlist same as below, but track_id is string 
@app_playlist.route("/playlist/<int:playlist_id>/track/<string:track_id>", methods=["POST"])
@auth_middleware
def add_track_to_playlist(playlist_id: int, track_id: str):
    try:
        playlist_content = playlist_repository.add_track_to_playlist(playlist_id, track_id)
        if playlist_content is None:
            return {
                "msg": "Could not add track to playlist"
            }, 400
        else:
            return playlist_content_schema.dump(playlist_content), 201
    except Exception as e:
        print(e)
        return {
            "msg": "Could not add track to playlist"
        }, 400

# delete track from playlist
@app_playlist.route("/playlist/<int:playlist_id>/track/<string:track_id>", methods=["DELETE"])
@auth_middleware
def delete_track_from_playlist(playlist_id: int, track_id: str):
    try:
        playlist_content = playlist_repository.delete_track_from_playlist(playlist_id, track_id)
        if playlist_content is None:
            return {
                "msg": "Could not delete track from playlist"
            }, 400
        else:
            return playlist_content_schema.dump(playlist_content)
    except Exception as e:
        print(e)
        return {
            "msg": "Could not delete track from playlist"
        }, 400
