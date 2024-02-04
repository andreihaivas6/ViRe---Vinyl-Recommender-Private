import json
from flask import current_app
from flask import request

import jwt
import json


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
        user_playlists = spotify_api.get_user_playlists()
        # print("User Playlists Number: ", len(user_playlists))

        # tracks_response = {}
        # tracks_response['track_name'] = []
        # tracks_response['artist_name'] = []
        # tracks_response['release_date'] = []

        # print("Trying to get the playlists tracks...")
        # for playlist in user_playlists:
        #     print(f"Playlist: {playlist['name']}")
        #     playlist_id = playlist["id"]
        #     playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)
        #     for track in playlist_tracks:
        #         tracks_response['track_name'].append(track[0])
        #         tracks_response['artist_name'].append(track[1])
        #         tracks_response['release_date'].append(track[2])
        #         print(f"Track: {track[0]}")

        tracks_response = list()
        for playlist in user_playlists:
            playlist_id = playlist["id"]

            playlist_tracks = spotify_api.get_playlist_tracks(playlist_id)
            for track in playlist_tracks:
                tracks_response.append({
                    "title": track[0],
                    "artist": track[1],
                    "date": str(track[2]).split("-")[0]
                })

        return tracks_response if response.status_code == 200 else {}
        
    @staticmethod
    def build_song_ids(ids):
        return ' '.join([f'<http://purl.org/ontology/mo/#song-{id}>' for id in ids])
    
    @staticmethod
    def get_tracklist(res: dict, track_dates: list = [], trackd_ids: list = []):
        dates_dict = {
            track_id: date 
            for track_id, date in zip(trackd_ids, track_dates)
        }
        result = list()
        try:
            for elem in res['result']['results']['bindings']:
                title = elem["title"]["value"]
                artist = elem["artist"]["value"]

                id = f"{title}-{artist}"
                id = id.replace(' ', '_').lower().replace('"', '').replace('.','').replace('\'', '').replace('<', '').replace('>', '')
                
                timestamp = dates_dict.get(id, "")
                timestamp = timestamp.strftime("%d/%m/%Y %H:%M") if timestamp else ""

                try:
                    genre = elem["genre"]["value"].replace("'", '"')
                    genre = json.loads(genre)
                    genre = ', '.join(genre)
                except:
                    genre = elem["genre"]["value"]
                
                result.append({
                    "track_id": id,
                    "title": title,
                    "artist": artist,
                    "genre": genre,
                    "duration": elem["duration"]["value"] if "duration" in elem else "",
                    "date": elem["date"]["value"] if "date" in elem else "",
                    "album": elem["album"]["value"] if "album" in elem else "",
                    "timestamp": timestamp
                })
            return result
        except Exception as e:
            print(e)
            return result