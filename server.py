"""Playlist creator."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import Artist, Song, Playlist, PlaylistSong, connect_to_db, db

import setlist_api
import spotify_api


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/create-playlist', methods=["GET"])
def show_create_playlist_form():
    """Shows create playlist page."""

    return render_template("create-playlist.html")

@app.route('/create-playlist', methods=["POST"])
def create_playlist():
    """Creates playlist in db."""

    playlist_title = request.form.get('playlist_title')
    setlist_api.create_playlist_in_db(playlist_title)

    flash(f'Playlist {playlist_title} created successfully.')
    return redirect('/')


@app.route('/display-playlists')
def display_playlists():
    """Show playlists on page."""
    if Playlist.query.first():
    #check if playlists have a query
        playlists = Playlist.query.all()
        return render_template("display-playlists.html", playlists=playlists)
    else:
        flash('No playlists to display.')
        return redirect('/')


@app.route('/add-to-playlist', methods=["GET"])
def show_add_to_playlist_form():
    """Shows page to add to playlists."""

    return render_template("add-to-playlist.html")

@app.route('/add-to-playlist', methods=["POST"])
def add_to_playlist():
    """Creates or updates playlist with songs."""
    playlist_title = request.form.get('playlist_title')
    artist_name = request.form.get('artist_name')

    artist = setlist_api.add_artist_to_db(artist_name)
    setlists = setlist_api.load_setlists_from_artist(artist)
    setlist_api.add_songs_to_db(artist, setlists)
    playlist = setlist_api.create_playlist_in_db(playlist_title)
    setlist_api.add_songs_to_playlist(artist,playlist)
    #remove when choosing songs

    flash(f'Songs added successfully to {playlist_title} playlist.')
    return redirect('/')


@app.route('/clear-playlists', methods=["GET"])
def show_clear_playlist_form():
    """Shows show_clear_playlist_form playlist page."""

    return render_template("clear-playlists.html")

@app.route('/clear-playlists', methods=["POST"])
def clear_playlist():
    """Deletes playlists from db."""

    PlaylistSong.query.delete()
    Playlist.query.delete()

    db.session.commit()

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

    app.run(port=5000, host='0.0.0.0')
