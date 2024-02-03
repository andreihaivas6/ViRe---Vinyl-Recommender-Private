from models import Playlist, PlaylistContent, TrackForJSPF
from main import db

from typing import List, Optional

from models import SharedPlaylist
from others import Utils

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
    
    def combine_playlists(self, first_playlist_id: int, second_playlist_id: int, method: str) -> Optional[Playlist]:
        try:
            first_playlist = Playlist.query.get(first_playlist_id)
            second_playlist = Playlist.query.get(second_playlist_id)

            if first_playlist is None or second_playlist is None:
                return None
            
            # user_id = Utils.get_user_id_from_token()
            # if first_playlist.user_id != user_id or second_playlist.user_id != user_id:
            #     return None
            
            if method == "intersection":
                combined_tracks = list(set(first_playlist.track_ids).intersection(second_playlist.track_ids))
            elif method == "difference":
                combined_tracks = list(set(first_playlist.track_ids).difference(second_playlist.track_ids))
            else:
                combined_tracks = list(set(first_playlist.track_ids).union(second_playlist.track_ids))

            combined_playlist = Playlist(
                user_id=first_playlist.user_id,
                user_name=first_playlist.user_name,
                playlist_name=f"{first_playlist.playlist_name} - {second_playlist.playlist_name}",
                playlist_description=f"Combined playlist: \n{first_playlist.playlist_description} - {second_playlist.playlist_description}",
                # track_ids=combined_tracks
            )

            db.session.add(combined_playlist)
            db.session.commit()

            for track in combined_tracks:
                playlist_content = PlaylistContent(
                    playlist_id=combined_playlist.playlist_id,
                    track_id=track
                )
                db.session.add(playlist_content)
            
            db.session.commit()

            return combined_playlist
        except Exception as e:
            print(e)
            return None

    def import_playlist(self, playlist: dict) -> Optional[Playlist]:
        try:
            imported_playlist = Playlist(
                user_id=Utils.get_user_id_from_token(),
                user_name=Utils.get_user_name_from_token(),
                playlist_name=playlist["title"],
                playlist_description="Imported playlist from JSPF file",
                imported_from_jspf=True
            )

            db.session.add(imported_playlist)
            db.session.commit()

            for track in playlist["track"]:
                track_for_jspf = TrackForJSPF(
                    playlist_id=imported_playlist.playlist_id,
                    title=track["title"],
                    artist=track["creator"],
                    album=track["album"]
                )
                db.session.add(track_for_jspf)
                db.session.commit()

            return imported_playlist
        except Exception as e:
            print(e)
            return None
