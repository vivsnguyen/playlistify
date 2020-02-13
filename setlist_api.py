"""Utility file for setlist.fm api."""
import requests
from sqlalchemy import func
from model import Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
from server import app

header_info = {'Accept' : 'application/json', 'x-api-key' : 'nrpEosh7l8AsjeWaokp9PZ4T2LYtkb2ctTS2'}

def add_artist_to_db(artist_name):
    """Adds artist to db."""
    artist = Artist(artist_name=artist_name)
    db.session.add(artist)
    db.session.commit()

def load_setlists_from_artist(artist_name):
    """Create a list of songs by chosen artist from a setlist."""
    #add tourName to params that defaults to None
    url = 'https://api.setlist.fm/rest/1.0/search/setlists'

    params_info = {'artistName':artist_name}

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


def create_playlist_in_db(playlist_title):
    # Playlist.query.delete()

    playlist = Playlist(playlist_title=playlist_title)

    db.session.add(playlist)
    db.session.commit()

#update playlist function

# if __name__ == "__main__":
#     connect_to_db(app)
#
#     # In case tables haven't been created, create them
#     db.create_all()
#
#     # Import different types of data
#     load_users()
#     load_movies()
#     load_ratings()
#     set_val_user_id()
