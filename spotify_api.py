"""Utility file for Spotify api."""
import os
import requests
import json
from sqlalchemy import func
from model import User, Artist, Song, Playlist, PlaylistSong
from model import connect_to_db, db
import server
import spotipy

header_info = {'Accept':'application/json',
    'Content-Type': 'application/json'}


#*******************
def spotify_authorization(username):

    scope = 'playlist-modify-private playlist-modify-public user-read-private streaming user-read-email user-modify-playback-state'

    token = spotipy.util.prompt_for_user_token(username, scope,
    client_id=os.environ['SPOTIPY_CLIENT_ID'],
    client_secret=os.environ['SPOTIPY_CLIENT_SECRET'],
    redirect_uri=os.environ['SPOTIPY_REDIRECT_URI'])

    if token:
        header_info['Authorization'] = f'Bearer {token}'
        sp = spotipy.Spotify(auth=token)
        return token
    else:
        print("Can't get token for", username)
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


    return response['id']

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

    if response['tracks']['items']:
        for i in range(len(response['tracks']['items'])):
            if response['tracks']['items'][i]['artists'][0].get('name') == artist_name:
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


def adjust_length_playlist(spotify_artist_id, filtered_track_uris):
    """If setlist songs < 10, add artist's top tracks uri's."""
    new_playlist = list(filtered_track_uris)
    if len(filtered_track_uris) < 10:
        top_tracks_uris = get_top_tracks_by_artist(spotify_artist_id)

        for track in top_tracks_uris:
            new_playlist.append(track)

    return new_playlist


def add_tracks_to_spotify_playlist(track_uris, playlist_id):
    """Adds songs to Spotify playlist via POST request."""

    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

    params_info = {'uris' : track_uris}

    response = requests.post(url,data=json.dumps(params_info),headers=header_info).json()

    return response

def create_spotify_playlist_from_db(user_id, playlist_title, spotify_username):
    """Process of creating playlist on spotify from db playlist."""


    playlist_id = create_playlist_on_spotify(playlist_title, spotify_username=spotify_username, public = False)

    track_uris = get_track_uris_from_user_playlist(user_id, playlist_title)

    # adjust_length_playlist(spotify_artist_id, filtered_track_uris)

    add_tracks_to_spotify_playlist(track_uris, playlist_id)

def start_user_playback(track_uris, device_id='11fcebde5061b2f96a395461dadd58c28b6a704e'):
    """Start/Resume a Spotify user's Playback."""


    url = 'https://api.spotify.com/v1/me/player/play'

    #get device id after activated through javascript? is it the same every time????
    query_info = {'device_id' : device_id}

    body_info = {'uris' : track_uris}

    response = requests.put(url, params=query_info,data=json.dumps(body_info),headers=header_info)


if __name__ == "__main__":
    connect_to_db(server.app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
