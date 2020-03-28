"""Utility file for Spotify api."""
import os
import requests
import json
import sys
import base64

from flask import request, flash, session

from sqlalchemy import func
from model import User, Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
import server
import spotipy

header_info = {'Accept':'application/json',
    'Content-Type': 'application/json'}

# Client keys
SPOTIFY_CLIENT_ID=os.environ['SPOTIPY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET=os.environ['SPOTIPY_CLIENT_SECRET']
# SPOTIFY_REDIRECT_URI='http://localhost:5000/spotify-callback'
SPOTIFY_REDIRECT_URI='http://54.218.47.102/spotify-callback'

# Spotify URLs
SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
SPOTIFY_AUTH_URL = 'https://accounts.spotify.com/authorize'
SPOTIFY_TOKEN_URL = 'https://accounts.spotify.com/api/token'
SPOTIFY_API_VERSION = 'v1'
SPOTIFY_API_URL = f'{SPOTIFY_API_BASE_URL}/{SPOTIFY_API_VERSION}'

SPOTIFY_SCOPE = 'playlist-modify-private playlist-modify-public user-read-private streaming user-read-email user-library-read user-modify-playback-state user-read-playback-state'

auth_query_param = {
    'response_type': 'code',
    'redirect_uri': SPOTIFY_REDIRECT_URI,
    'scope': SPOTIFY_SCOPE,
    'client_id': SPOTIFY_CLIENT_ID
}

def generate_auth_url():
    """ Returns user authorization url.
    Used in '/spotify-login' route. """

    spotify_auth_url = (SPOTIFY_AUTH_URL + '?client_id=' + auth_query_param['client_id'] +
                        '&response_type=' + auth_query_param['response_type'] +
                        '&redirect_uri=' + auth_query_param['redirect_uri'] +
                        '&scope=' + auth_query_param['scope'])

    return spotify_auth_url

def get_auth_token():
    """ Returns authorization token from Spotify.
    Used in '/spotify-callback' route. """

    auth_code = request.args['code']

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_code),
        "redirect_uri": SPOTIFY_REDIRECT_URI
    }

    base64encoded = base64.b64encode(("{}:{}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    return post_request.json()

def get_new_auth_token(refresh_token):
    """ Takes in refresh token from exisiting user to generate a new authorization token. """

    code_payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

    base64encoded = base64.b64encode(("{}:{}".format(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    return post_request.json()

def auth_header(token):
    """Sets header dict to include Spotify's authorization token. """
    header_info["Authorization"] = f"Bearer {token}"

def get_spotify_user_id():
    """ Return user's spotify ID.  """

    request = "{}/{}".format(SPOTIFY_API_URL, 'me')
    user_info = requests.get(request, headers=header_info).json()
    spotify_user_id = user_info['id']

    return spotify_user_id
#*******************
# def spotify_authorization(username):
#
#     scope = 'playlist-modify-private playlist-modify-public user-read-private streaming user-read-email user-modify-playback-state'
#
#     token = spotipy.util.prompt_for_user_token(username, scope,
#     client_id=os.environ['SPOTIPY_CLIENT_ID'],
#     client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
#     redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])
#
#     if token:
#         header_info['Authorization'] = f'Bearer {token}'
#         sp = spotipy.Spotify(auth=token)
#         return token
#     else:
#         print("Can't get token for", username)
#********************

def create_playlist_on_spotify(playlist_title, spotify_username, public = False):
    """Create a playlist on Spotify and return its id."""
    url = f'https://api.spotify.com/v1/users/{spotify_username}/playlists'

    params_info = {
      "name": playlist_title,
      #"description": "New playlist description",
      "public": 'false'
    }

    response = requests.post(url,data=json.dumps(params_info),headers=header_info).json()

    spotify_playlist_id = response['id']

    return spotify_playlist_id

def get_artist_id_by_artist_name(artist_name):
    """
    Get artist's Spotify id by artist name.

    >>> artist = get_artist_id_by_artist_name('boy pablo')

    >>> print(artist)
    7wbkl3zgDZEoZer357mVIw
    """

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

    artist_id = get_artist_id_by_artist_name(artist_name)

    if response.get('tracks'):
        if response['tracks']['items']:
            for i in range(len(response['tracks']['items'])):
                if response['tracks']['items'][i]['artists'][0].get('id') == artist_id:
                    return response['tracks']['items'][i]['uri']
                else:
                    continue

def get_top_tracks_by_artist(spotify_artist_id):
    """Get the Spotify track URI's of an artist's top 5 tracks."""

    track_uris = []

    if spotify_artist_id:
        url = f'https://api.spotify.com/v1/artists/{spotify_artist_id}/top-tracks'

        params_info = {'country': 'US'}

        response = requests.get(url,params=params_info,headers=header_info).json()

        if response.get('tracks'):
            for i in range(5):
                track_uris.append(response['tracks'][i]['uri'])

    return track_uris

def get_track_uris_from_user_playlist(user_id, playlist_title):
    """Return Spotify track URI's from user's playlist in db."""

    playlist = Playlist.query.filter_by(playlist_title = playlist_title, user_id=user_id).first()

    track_uris = []

    if playlist.songs:
        for song in playlist.songs:
            artist_name = Artist.query.get(song.primary_artist).artist_name

            track_uris.append(get_song_uri_by_song_name(song.song_name, artist_name))

    filtered_track_uris = [uri for uri in track_uris if uri != None]

    return filtered_track_uris

def get_spotify_artist_id_from_track_uri(track_uri):
    """(helper function for adjust_length_playlist)"""

    id = track_uri[14:]
    url = f'https://api.spotify.com/v1/tracks/{id}'

    response = requests.get(url,headers=header_info).json()

    spotify_artist_id = response['artists'][0]['id']

    return spotify_artist_id

#FIX********
def adjust_length_playlist(filtered_track_uris):
    """If setlist songs < 10, add artist's top tracks uri's."""

    new_playlist = list(filtered_track_uris)
    if len(filtered_track_uris) < 10:
        #this assumes that all tracks on list from same artist
        spotify_artist_id = get_spotify_artist_id_from_track_uri(filtered_track_uris[0])
        top_tracks_uris = get_top_tracks_by_artist(spotify_artist_id)

        for track in top_tracks_uris:
            new_playlist.append(track)

    return new_playlist
#*******************

def add_tracks_to_spotify_playlist(track_uris, playlist_id):
    """Adds songs to Spotify playlist via POST request."""

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    params_info = {'uris' : track_uris}

    response = requests.post(url,data=json.dumps(params_info),headers=header_info).json()

    return response

def create_spotify_playlist_from_db(user_id, playlist_title, token):
    """Process of creating playlist on spotify from db playlist."""

    auth_header(token)

    spotify_username = get_spotify_user_id()

    playlist_id = create_playlist_on_spotify(playlist_title, spotify_username=spotify_username, public = False)

    track_uris = get_track_uris_from_user_playlist(user_id, playlist_title)

    adjusted_playlist_uris = adjust_length_playlist(track_uris)

    add_tracks_to_spotify_playlist(adjusted_playlist_uris, playlist_id)

def get_user_devices():
    url = f'{SPOTIFY_API_URL}/me/player/devices'

    response = requests.get(url,headers=header_info).json()

    devices_list = response['devices']

    for device in devices_list:
        if device['name'] == 'Playlist Web Player thingy':
            web_device_id = device['id']
        else:
            web_device_id = None

    return web_device_id

def start_user_playback(track_uris, device_id):
    """Start/Resume a Spotify user's Playback."""


    url = 'https://api.spotify.com/v1/me/player/play'

    #get device id after activated through javascript? is it the same every time????
    query_info = {'device_id' : device_id}

    body_info = {'uris' : track_uris}

    response = requests.put(url, params=query_info,data=json.dumps(body_info),headers=header_info)


def play_playlist_on_web_player(user_id, playlist_title, token):
    """Play chosen playlist on web player."""

    auth_header(token)

    device_id = get_user_devices()

    track_uris = get_track_uris_from_user_playlist(user_id, playlist_title)

    start_user_playback(track_uris=track_uris, device_id=device_id)

if __name__ == "__main__":
    connect_to_db(server.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
