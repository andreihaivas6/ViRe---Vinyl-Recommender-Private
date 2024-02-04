import requests

class SpotifyAPI:
    def __init__(self, access_token):
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {access_token}"
        }

    def get_user_playlists(self):
        try:
            url = "https://api.spotify.com/v1/me/playlists"
            response = requests.get(url, headers=self.headers)
            playlists = response.json().get("items", [])
            return playlists
        except Exception as e:
            print(e)
            return []

    def decode_response(self, response):
        try:
            tracks = []
            for i in range(0, len(response)):
                tracks.append((response[i]['track']['name'], response[i]['track']['artists'][0]['name'], response[i]['track']['album']['release_date']))
         
            return tracks
        except Exception as e:
            print(e)
            return None

    def get_playlist_tracks(self, playlist_id):
        try:
            url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        
            response = requests.get(url, headers=self.headers)
            tracks = response.json().get("items", [])
            tracks = self.decode_response(tracks)
        except Exception as e:
            print(e)
        return tracks
