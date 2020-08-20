"""Playlist creator project."""

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    playlists = db.relationship("Playlist", backref="user")

    def __repr__(self):

        return f"<User id={self.id}, name={self.name}>"

class Artist(db.Model):
    """Artists chosen by user"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Artist artist_name={self.artist_name}>"


class Song(db.Model):
    """Songs from setlists of chosen artist."""

    __tablename__ = "songs"
    __table_args__ = (db.UniqueConstraint('primary_artist', 'song_name'),)


    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_name = db.Column(db.String(200), nullable=True)
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

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    songs = db.relationship("Song", secondary="playlist_songs", backref="playlists")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Playlist playlist_title={self.playlist_title}>"


class PlaylistSong(db.Model):
    """Song of playlist.


    1 playlist_song has 1 playlist
    1 playlist has many playlist_songs
    """

    __tablename__ = 'playlist_songs'

    playlist_song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.playlist_id'))
    song_id = db.Column(db.Integer, db.ForeignKey('songs.song_id'))

    def __repr__(self):
        return f"<PlaylistSong artist_id={self.artist_id} song_id={self.song_id}>"

# def clear_data():
#     PlaylistSong.query.delete()
#     Playlist.query.delete()
#     Song.query.delete()
#     Artist.query.delete()
#
#     db.session.commit()

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    PlaylistSong.query.delete()
    Playlist.query.delete()
    Song.query.delete()
    Artist.query.delete()
    User.query.delete()

    # Add sample data

    artist = Artist(artist_name='boy pablo')
    user = User(name='vivivi.n', email='vivi@vivi.com', password_hash='hello')
    playlist = Playlist(playlist_title='party time')

    db.session.add_all([artist, user,playlist])
    db.session.commit()

def delete_user_playlist(playlist_title, user_id):
    """Delete a user's playlist."""

    playlist = Playlist.query.filter_by(playlist_title = playlist_title, user_id=user_id).first()

    db.session.delete(playlist)
    db.session.commit()

def delete_playlist(playlist_title, user_id):
    user = User.query.get(user_id)
    #get playlist obj by query playlist title
    #check if playlist.user_id matches with session user_id else not authorized

    db.session.delete(user.playlists[0])
    db.session.commit()

##############################################################################
# Helper functions


def connect_to_db(app, db_uri="postgresql:///playlist-creator"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")
