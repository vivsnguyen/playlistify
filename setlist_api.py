"""Utility file for setlist.fm api."""
import os
import requests
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from model import User, Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
import server
# from server import app


header_info = {'Accept' : 'application/json', 'x-api-key' : os.environ['SETLIST_FM_API_KEY']}

def add_artist_to_db(artist_name):
    """Adds artist to db if not already in db. Returns artist db object.
    
    >>> add_artist_to_db('boy pablo')
    <Artist artist_name=boy pablo>
    """
    if not Artist.query.filter_by(artist_name=artist_name).first():
        artist = Artist(artist_name=artist_name)
        db.session.add(artist)
        db.session.commit()

    else:
        artist = Artist.query.filter_by(artist_name=artist_name).first()

    return artist


def load_setlists_from_artist(artist):
    """Create a list of songs by chosen artist from a setlist.

    >>> artist = add_artist_to_db('boy pablo')
    >>> load_setlists_from_artist(artist) #doctest: +ELLIPSIS
    [...]

    """

    #add tourName to params that defaults to None
    url = 'https://api.setlist.fm/rest/1.0/search/setlists'

    params_info = {'artistName':artist.artist_name}

    response = requests.get(url,params=params_info,headers=header_info).json()

    #a list of dicts
    if response.get('setlist') is None:
        return []
    else:
        setlist_list = response['setlist']


    setlist_num = 0

    chosen_setlist = setlist_list[setlist_num]['sets']['set']

    while not chosen_setlist: #while the setlist is empty
        if chosen_setlist:
            break
        else:
            setlist_num += 1
            chosen_setlist = setlist_list[setlist_num]['sets']['set']

    chosen_setlist = setlist_list[setlist_num]['sets']['set'][0]['song']

    db_setlist_list = []
    for song in chosen_setlist:
        db_setlist_list.append(song['name'])

    return db_setlist_list


def add_songs_to_db(artist, db_setlist_list):
    """Add songs from list of strings to db with primary_artist id."""
    if db_setlist_list:
        for song in db_setlist_list:
            try:
                artist.songs.append(Song(song_name = song))
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                continue

# def check_if_user_has_playlists(user_id):


def create_playlist_in_db(playlist_title, user_id):
    """Creates playlist in db if not already in db."""
    user = User.query.get(user_id)

    #check if user logged in
    #check if no user, no playlists
    #check if user has no playlists

    if not Playlist.query.filter_by(playlist_title=playlist_title, user_id=user_id).first():
        playlist = Playlist(playlist_title=playlist_title)
        user.playlists.append(playlist)

        db.session.commit()

    else:
        playlist = Playlist.query.filter_by(playlist_title=playlist_title).first()

    return playlist


def add_songs_to_playlist(artist, user_id, playlist):
    """Add songs from Artist object to Playlist object in db."""
    user = User.query.get(user_id)

    # for user_playlist in user.playlists:
    #     if user_playlist.playlist_title == playlist.playlist_title:
    #         playlist = user_playlist

    for song in artist.songs:
        playlist.songs.append(song)

    db.session.commit()


def db_create_playlist(artist_name, playlist_title, user_id):
    artist = add_artist_to_db(artist_name)
    setlists = load_setlists_from_artist(artist)
    add_songs_to_db(artist, setlists)
    playlist = create_playlist_in_db(playlist_title, user_id)
    add_songs_to_playlist(artist, user_id, playlist)


if __name__ == "__main__":
    connect_to_db(app.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()

    from doctest import testmod
    if testmod().failed == 0:
        print("Setlist API tests passed.")
