"""Playlist creator."""
import os
import requests
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Artist, Song, Playlist, PlaylistSong, clear_data, connect_to_db, db

import spotipy

import setlist_api
import spotify_api





app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/spotify-account')
def spotify_account():
    return render_template("spotify-account.html")

#**********************
@app.route('/spotify-authorize')
def spotify_authorize():
    """"""

    username = request.args.get('username')
    spotify_api.spotify_authorization(username)
#************************


@app.route('/display-playlists')
def display_playlists():
    """Show playlists on page."""

    if Playlist.query.first():
    #check if playlists have a query
        playlists = Playlist.query.all()
        return render_template("display-playlists.html", playlists=playlists)
    else:
        return 'No playlists to display.'


@app.route('/add-to-playlist', methods=["GET"])
def show_add_to_playlist_form():
    """Shows page to add to playlists."""

    return render_template("add-to-playlist.html")

@app.route('/add-to-playlist', methods=["POST"])
def add_to_playlist():
    """Creates or updates playlist with songs."""
    playlist_title = request.form.get('playlist_title')
    artist_name = request.form.get('artist_name')

    setlist_api.create_playlist(artist_name, playlist_title)

    flash(f'Songs added successfully to {playlist_title} playlist.')
    return redirect('/')

#*********************************
@app.route('/add-to-spotify-playlist', methods=["POST"])
def add_to_spotify_playlist():
    """Adds playlist to spotify."""
    #get playlist title from jinja loop
    playlist_title = request.form.get('playlist_title')

    # spotify_api.create_spotify_playlist_from_db(playlist_title) #need to get spotify user_id, public or private?
    flash(f'Songs added successfully to {playlist_title} playlist on Spotify.')
    return redirect('/')
#************************************


@app.route('/clear-playlists', methods=["GET"])
def show_clear_playlist_form():
    """Shows show_clear_playlist_form playlist page."""

    return render_template("clear-playlists.html")

@app.route('/clear-playlists', methods=["POST"])
def clear_playlist():
    """Deletes playlists from db."""

    clear_data()

    flash('All playlists deleted.')
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False #for error: AttributeError: 'Request' object has no attribute 'is_xhr'

    app.run(port=5000, host='0.0.0.0')
