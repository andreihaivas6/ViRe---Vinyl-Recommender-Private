from flask import current_app
from flask import request
import requests
import jwt

from repositories import UserRepository

class Utils:
    @staticmethod
    def get_token():
        return request.headers.get("Authorization").split(" ")[1]
    
    @staticmethod
    def get_user_from_token(token):
        try:
            data = jwt.decode(
                token, 
                current_app.config["SECRET_KEY"], 
                algorithms=["HS256"]
            )
            user_id = data["id"]

            user = UserRepository.get_user_by_id(user_id)
            return user
        except:
            return None
    
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
    def get_tracks(playlists, headers):
        tracks = []
        for playlist in playlists:
                playlist_id = playlist["id"]
                playlist_name = playlist["name"]
                print(f"Playlist: {playlist_name}")
                response = requests.get(
                    f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", 
                    headers=headers
                )
                tracks += response.json()["items"]
                for track in tracks:
                    track_name = track["track"]["name"]
                    artists = track["track"]["artists"]
                    print(f"Track: {track_name}")
                    for artist in artists:
                        artist_name = artist["name"]
                        print(f"Artist: {artist_name}")
                print()
        return tracks
    
    @staticmethod
    def get_spotify_user_info(access_token: str):
        try:
            headers = {
                "Authorization": f"Bearer {access_token.strip()}"
            }
            response = requests.get(
                "https://api.spotify.com/v1/me/playlists", 
                headers=headers
            )
            playlists = response.json()["items"]

            tracks = Utils.get_tracks(playlists, headers)
            return tracks

        except Exception as e:
            print(e)
            return None
