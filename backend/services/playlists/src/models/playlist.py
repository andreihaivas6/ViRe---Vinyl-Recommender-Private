from datetime import datetime, timedelta
from main import db, ma

from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import fields

class PlaylistContent(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)

    __tablename__ = "playlist_content"

    playlist_content_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), nullable=False)
    track_id = db.Column(db.String, nullable=False)

    playlists = db.relationship("Playlist", back_populates="playlist_content", foreign_keys=[playlist_id])

    __table_args__ = (
        db.UniqueConstraint("playlist_id", "track_id", name="unique_playlist_content"),
    )

class Playlist(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    user_id = db.Column(db.Integer, nullable=False)
    playlist_name = db.Column(db.String, nullable=False)
    imported_from_jspf = db.Column(db.Boolean, nullable=False, default=False)

    playlist_description = db.Column(db.String, nullable=True)
    user_name = db.Column(db.String, nullable=True)

    playlist_content = db.relationship("PlaylistContent", back_populates="playlists", lazy=False)
    
    @hybrid_property
    def track_ids(self):
        return [content.track_id for content in self.playlist_content]

    def to_json(self):
        return {
            "playlist_id": self.playlist_id,
            "user_id": self.user_id,
            "playlist_name": self.playlist_name,
            "playlist_description": self.playlist_description,
            "user_name": self.user_name,
            "imported_from_jspf": self.imported_from_jspf,
            "track_ids": self.track_ids,
            # "playlist_content": self.playlist_content
        }


class SharedPlaylist(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)

    __tablename__ = "shared_playlists"

    shared_playlist_id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), nullable=False)
    shared_with_user_name = db.Column(db.String, nullable=False)

    playlists = db.relationship("Playlist", foreign_keys=[playlist_id])

    __table_args__ = (
        db.UniqueConstraint("playlist_id", "shared_with_user_name", name="unique_shared_playlist"),
    )

class TrackForJSPF(db.Model):
    def local_time():
        return datetime.utcnow() + timedelta(hours=2)

    __tablename__ = "tracks_for_jspf"

    track_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.playlist_id"), nullable=True)
    title = db.Column(db.String, nullable=True)
    artist = db.Column(db.String, nullable=True)
    album = db.Column(db.String, nullable=True)

    def to_json(self):
        return {
            "track_id": self.track_id,
            "playlist_id": self.playlist_id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album
        }

class PlaylistContentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PlaylistContent
        load_instance = True
        sqla_session = db.session
        include_fk = True

class PlaylistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Playlist
        load_instance = True
        sqla_session = db.session
        exclude = ("user_id",)

class PlaylistSchemaWithContent(ma.SQLAlchemyAutoSchema):
    track_ids = fields.Method("get_track_ids")

    def get_track_ids(self, playlist):
        return playlist.track_ids

    class Meta:
        model = Playlist
        load_instance = True
        sqla_session = db.session
        # exclude = ("user_id",)
        include_relationships = True 

class SharedPlaylistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SharedPlaylist
        load_instance = True
        sqla_session = db.session
        include_fk = True


playlist_schema = PlaylistSchema()
playlists_schema = PlaylistSchema(many=True)

playlist_schema_with_content = PlaylistSchemaWithContent()
playlists_schema_with_content = PlaylistSchemaWithContent(many=True)

playlist_content_schema = PlaylistContentSchema()
playlist_contents_schema = PlaylistContentSchema(many=True)

shared_playlist_schema = SharedPlaylistSchema()
shared_playlists_schema = SharedPlaylistSchema(many=True)
