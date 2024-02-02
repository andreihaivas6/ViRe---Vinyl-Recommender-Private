from models import Playlist, PlaylistContent
from main import db

from typing import List, Optional

from models import SharedPlaylist

class PlaylistActionsRepository:
    def __init__(self):
        self.db = db
    
    def share_playlist_id_with_user_id(self, user_id: int, shared_playlist: SharedPlaylist) -> Optional[Playlist]:
        try:
            playlist = Playlist.query.get(shared_playlist.playlist_id)
            if playlist is None:
                return None
            
            # check if playlist is owned by the given user
            if playlist.user_id != user_id:
                return None
            
            # check if playlist is already shared with the given user
            if playlist.user_name == shared_playlist.shared_with_user_name:
                return None

            db.session.add(shared_playlist)
            db.session.commit()

            return playlist
        except Exception as e:
            return None
