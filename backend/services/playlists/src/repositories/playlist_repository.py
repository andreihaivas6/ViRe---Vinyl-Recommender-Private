from models import Playlist, PlaylistContent, SharedPlaylist, TrackForJSPF
from main import db

from typing import List, Optional

class PlaylistRepository:
    def __init__(self):
        self.db = db
    
    def get_playlist_by_id(self, playlist_id: int) -> Optional[Playlist]:
        try:
            playlist = Playlist.query.get(playlist_id)
            return playlist
        except Exception as e:
            return None
    
    def get_playlists_of_user_id(self, user_id: int) -> List[Playlist]:
        playlists = Playlist.query.filter_by(user_id=user_id).all()
        return playlists
    
    def get_playlists_with_username(self, username: str) -> List[Playlist]:
        playlists = Playlist.query.filter_by(username=username).all()
        return playlists
    
    def get_playlists_shared_with_username(self, username: str) -> List[Playlist]:
        shared_playlists = SharedPlaylist.query.filter_by(shared_with_user_name=username).all()
        playlists = [
            Playlist.query.get(shared_playlist.playlist_id)
            for shared_playlist in shared_playlists
        ]
        return playlists


    def create_playlist(self, playlist: Playlist) -> Optional[Playlist]:
        try:
            db.session.add(playlist)
            db.session.commit()

            return playlist
        except Exception as e:
            print(e)
            return None
    
    def delete_playlist(self, playlist_id: int) -> Optional[Playlist]:
        try:
            playlist = Playlist.query.get(playlist_id)
            if playlist is None:
                return None
            
            db.session.delete(playlist)
            db.session.commit()

            return playlist
        except Exception as e:
            return None
    
    def add_track_to_playlist(self, playlist_id: int, track_id: str) -> Optional[Playlist]:
        try:
            playlist = Playlist.query.get(playlist_id)
            if playlist is None:
                return None
            
            playlist_content = PlaylistContent(
                playlist_id=playlist_id,
                track_id=track_id
            )
            
            db.session.add(playlist_content)
            db.session.commit()

            return playlist_content
        except Exception as e:
            return None
    
    def delete_track_from_playlist(self, playlist_id: int, track_id: str) -> Optional[Playlist]:
        try:
            playlist_content = PlaylistContent.query.filter_by(playlist_id=playlist_id, track_id=track_id).first()
            if playlist_content is None:
                return None
            
            db.session.delete(playlist_content)
            db.session.commit()

            return playlist_content
        except Exception as e:
            return None
    
    def add_track_to_jspf_playlist(self, playlist: Playlist) -> Optional[Playlist]:
        try:
            tracks = TrackForJSPF.query.filter_by(playlist_id=playlist.playlist_id).all()
            tracks = [
                track.to_json()
                for track in tracks
            ]

            playlist_result = playlist.to_json()
            playlist_result["tracks"] = tracks

            return playlist_result
        except Exception as e:
            return None
    