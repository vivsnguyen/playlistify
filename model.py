"""Playlist creator project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class Artist(db.Model):
    """Artists chosen by user"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Artist artist_name={self.artist_name}>"


class Song(db.Model):
    """Songs from setlists of chosen artist."""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(80), nullable=True)
    primary_artist = db.Column(db.Integer, db.ForeignKey('artists.artist_id'))

    artist = db.relationship("Artist", backref="songs")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Song song_name={self.song_name} Artist primary_artist={self.primary_artist}>"


class Playlist(db.Model):
    """Playlist created by user."""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_title = db.Column(db.String(80), nullable=True)

    songs = db.relationship("Song", secondary="playlist_songs", backref="playlists")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Playlist playlist_title={self.playlist_title}>"


class PlaylistSong(db.Model):
    """Song of playlist."""

    """
    1 playlist_song has 1 playlist
    1 playlist has many playlist_songs
    """

    __tablename__ = 'playlist_songs'

    playlist_song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))

    def __repr__(self):
        return f"<PlaylistSong artist_id={self.artist_id} song_id={self.song_id}>"

##############################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///playlist-creator'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
