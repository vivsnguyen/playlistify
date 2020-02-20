"""Utility file for Spotify api."""
import requests
from sqlalchemy import func
from model import Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
import server
from secrets import spotify_api_key, spotify_client_id

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


def get_song_uri_by_song_name(song_name, artist_name):
    """
    Get a track's Spotify URI by song name and artist name.

    >>> get_song_uri_by_song_name('everytime','boy pablo')

    'spotify:track:4zvHZWOGyL7WcmqHOgtGCW'
    """

    url = 'https://api.spotify.com/v1/search'

    params_info = {'q': song_name, 'type' : 'track'}

    response = requests.get(url,params=params_info,headers=header_info).json()

    if response['tracks']['items']:
        for i in range(len(response['tracks']['items'])):
            if response['tracks']['items'][i]['artists'][0].get('name') == artist_name:
                return response['tracks']['items'][0]['uri']


def get_top_tracks_by_artist(spotify_artist_id):
    """Get the Spotify track URI's of an artist's top 5 tracks."""

    track_uris = []

    if spotify_artist_id:
        url = f'https://api.spotify.com/v1/artists/{id}/top-tracks'

        params_info = {'id': spotify_artist_id, 'country': 'US'}

        response = requests.get(url,params=params_info,headers=header_info).json()

        for i in range(5):
            track_ids.append(response['tracks'][i]['uri'])

    return track_uris

def get_track_uris_from_user_playlist(playlist_title):
    """Return Spotify track URI's from user's playlist in db."""

    playlist = Playlist.query.filter_by(playlist_title = playlist_title).first()

    track_uris = []

    if playlist.songs:
        for song in playlist.songs:
            artist_name = Artist.query.get(song.primary_artist).artist_name

            track_uris.append(get_song_uri_by_song_name(song.song_name, artist_name))

    return track_uris

def request_authorization():
    url = 'https://accounts.spotify.com/authorize'

    params_info = {'client_id' : spotify_client_id,
                    'response_type' : 'code',
                    'redirect_uri' : 'http://0.0.0.0:5000/',
                    'scope' : 'playlist-read-private'}

    response = requests.get(url,params=params_info)

if __name__ == "__main__":
    connect_to_db(server.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
