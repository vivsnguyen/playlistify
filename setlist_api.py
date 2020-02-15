"""Utility file for setlist.fm api."""
import requests
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from model import Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
import server
# from server import app

header_info = {'Accept' : 'application/json', 'x-api-key' : 'nrpEosh7l8AsjeWaokp9PZ4T2LYtkb2ctTS2'}

def add_artist_to_db(artist_name):
    """Adds artist to db if not already in db."""
    if not Artist.query.filter_by(artist_name=artist_name).first():
        artist = Artist(artist_name=artist_name)
        db.session.add(artist)
        db.session.commit()

    else:
        artist = Artist.query.filter_by(artist_name=artist_name).first()

    return artist


def load_setlists_from_artist(artist): #could take in artist ID or artist object
    """Create a list of songs by chosen artist from a setlist."""
    #add tourName to params that defaults to None
    url = 'https://api.setlist.fm/rest/1.0/search/setlists'

    params_info = {'artistName':artist.artist_name}

    response = requests.get(url,params=params_info,headers=header_info).json()

    #a list of dicts
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

    for song in db_setlist_list:
        try:
            artist.songs.append(Song(song_name = song))
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            continue
    return


def create_playlist_in_db(playlist_title):
    """Creates playlist in db if not already in db."""
    if not Playlist.query.filter_by(playlist_title=playlist_title).first():
        playlist = Playlist(playlist_title=playlist_title)
        db.session.add(playlist)
        db.session.commit()

    else:
        playlist = Playlist.query.filter_by(playlist_title=playlist_title).first()

    return playlist


def add_songs_to_playlist(artist,playlist):
    """Add songs from Artist object to Playlist object in db."""

    for song in artist.songs:
        playlist.songs.append(song)
    db.session.commit()

    return

if __name__ == "__main__":
    connect_to_db(server.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
