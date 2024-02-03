import json
from flask import current_app
from flask import request

import jwt

class Utils:
    @staticmethod
    def get_token():
        return request.headers.get("Authorization").split(" ")[1]
    from flask import current_app
from flask import request
import requests
import jwt

from .spotify_api import SpotifyAPI

class Utils:
    @staticmethod
    def get_token():
        return request.headers.get("Authorization").split(" ")[1]
    
    @staticmethod
    def get_user_id_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["id"]
        except:
            return None
    
    @staticmethod
    def get_user_name_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["username"]
        except:
            return "no-name"
    
    
    @staticmethod
    def get_spotify_user_info(access_token: str):
        access_token = access_token.strip()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(
            "https://api.spotify.com/v1/me",
            headers=headers
        )

        spotify_api = SpotifyAPI(access_token)
        # Get User Playlists
        user_playlists = spotify_api.get_user_playlists()
        tracks_response = {}
        tracks_response['track_name'] = []
        tracks_response['artist_name'] = []
        tracks_response['release_date'] = []

        for playlist in user_playlists:
            playlist_id = playlist["id"]
            playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)
            for track in playlist_tracks:
                tracks_response['track_name'].append(track[0])
                tracks_response['artist_name'].append(track[1])
                tracks_response['release_date'].append(track[2])

        return json.dumps(tracks_response) if response.status_code == 200 else None
       


    @staticmethod
    def get_user_id_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["id"]
        except:
            return None
    
    @staticmethod
    def get_user_name_from_token():
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            return data["username"]
        except:
            return "no-name"
