from models import Playlist, PlaylistContent
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
    