"""Utility file for Spotify api."""
import requests
from sqlalchemy import func
from model import Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
from secrets import spotify_api_key

header_info = {'Accept':'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {spotify_api_key}'}

def get_artist_id_by_artist_name(artist_name):
    """Get artist's Spotify id by artist name."""

    url = 'https://api.spotify.com/v1/search'
    params_info = {'q': artist_name, 'type' : 'artist'}
    response = requests.get(url,params=params_info,headers=header_info).json()

    if response['artists']['items']:
        spotify_artist_id = response['artists']['items'][0]['id'] #['artists']['items'][0] gives first search result

    else:
        return None
    return spotify_artist_id

# def get_song_id_by_song_name(song_name, artist_name):
#     #check if song searched matches with artist in db
#

def get_top_tracks_by_artist(spotify_artist_id):
    """Get the Spotify id's of an artist's top 5 tracks."""

    track_ids = []

    if spotify_artist_id:
        url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'

        params_info = {'id': spotify_artist_id, 'country': 'US'}

        response = requests.get(url,params=params_info,headers=header_info).json()

        for i in range(5):
            track_ids.append('spotify:track:' + response['tracks'][i]['id'])

    return track_ids

if __name__ == "__main__":
    connect_to_db(server.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
