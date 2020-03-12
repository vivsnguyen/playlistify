"""Playlist creator."""
import os
import requests
from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Artist, Song, Playlist, PlaylistSong, delete_user_playlist, connect_to_db, db
# clear_data

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

#************************************************
#Spotify Authorization
# @app.route('/spotify-account')
# def spotify_account():
#     return render_template("spotify-account.html")

# @app.route('/spotify-authorize')
# def spotify_authorize():
#     """"""
#     if session.get("spotify username"):
#         del session["spotify username"]
#
#     username = request.args.get('username')
#     session['spotify username'] = username
#     spotify_api.spotify_authorization(username)
#
#     return redirect('/') #??????

@app.route('/spotify-login')
def spotify_login():
    """ Spotify Authorization Page """


    spotify_auth_url = spotify_api.generate_auth_url()
    print('\n\n\n\n')
    print(spotify_auth_url)

    return redirect(str(spotify_auth_url))

@app.route('/spotify-callback')
def spotify_callback():
    spotify_response_data = spotify_api.get_auth_token()
    session['access_token'] = spotify_response_data.get('access_token')
    session['refresh_token'] = spotify_response_data.get('refresh_token')

    print(session.items())

    #return render_template('display-tokens.html')
    return redirect('/')

#************************************************

@app.route('/display-playlists')
def display_playlists():
    """Show playlists on page."""
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    return render_template("display-playlists.html", playlists=user.playlists)


@app.route('/add-to-playlist', methods=["GET"])
def show_add_to_playlist_form():
    """Shows page to add to playlists."""

    return render_template("add-to-playlist.html")

@app.route('/add-to-playlist', methods=["POST"])
def db_add_to_playlist():
    """Adds to playlist in db."""

    playlist_title = request.form.get('playlist_title')
    artist_name = request.form.get('artist_name')

    user_id = session.get("user_id")

    setlist_api.db_create_playlist(artist_name = artist_name, playlist_title = playlist_title, user_id = user_id)


    flash(f'Songs added successfully to {playlist_title} playlist.')
    return redirect(f'/user-dashboard/{user_id}')

#*********************************
@app.route('/add-to-spotify-playlist', methods=["POST"])
def add_to_spotify_playlist():
    """Adds playlist to spotify."""
    user_id = session.get("user_id")
    playlist_title = request.form.get('playlist_title')
    spotify_username = session.get('spotify username')

    #check if token in session?
    token = session.get('access_token')

    spotify_api.create_spotify_playlist_from_db(user_id, playlist_title, token)
    #need to get spotify user_id, public or private?
    flash(f'Songs added successfully to {playlist_title} playlist on Spotify.')
    return redirect(f'/user-dashboard/{user_id}')
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

@app.route('/delete-playlist', methods=["POST"])
def delete_playlist():
    """Deletes playlist from db."""
    playlist_title = request.form.get('playlist_title')
    user_id = session.get('user_id')

    delete_user_playlist(playlist_title, user_id)

    flash(f'Playlist {playlist_title} deleted.')
    return redirect(f'/user-dashboard/{user_id}')

@app.route("/log-in", methods=["GET"])
def show_login_form():
    """Show login form or registration button for users."""

    user_id = session.get("user_id")

    if user_id:
        return redirect(f"/user-dashboard/{user_id}")

    return render_template("user-login.html")


@app.route("/log-in", methods=["POST"])
def handle_login():
    """Log-in a user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash(f"No account with {email}.")
        return redirect("/log-in")

    if not user.check_password(password):
        flash("Incorrect password.")
        return redirect("/log-in")

    session["user_id"] = user.id
    flash("Login successful.")
    return redirect(f"/user-dashboard/{user.id}")

@app.route("/register", methods=["GET"])
def show_registration_form():
    """Show registration form for users."""

    return render_template("user-register.html")


@app.route("/register", methods=["POST"])
def process_user_registration():
    """Process user registration."""

    username = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if User.query.filter_by(email=email).first():
        flash("An account with this email already exists.")
        return redirect("/register")

    new_user = User(name=username, email=email)

    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    # Log in new user
    session["user_id"] = new_user.id

    flash(f"Successfully registered {username}.")
    return redirect(f"/user-dashboard/{new_user.id}")



@app.route("/logout")
def logout():
    """Log out of a user account."""

    session.clear()
    flash("Logout successful.")

    return redirect("/")


@app.route("/user-dashboard/<int:user_id>")
def show_user_dashboard(user_id):
    """Show a user's dashboard where they can view and play playlists."""

    if check_authorization(user_id):
        user = User.query.get(user_id)
        playlists = user.playlists

        return render_template("user-dashboard.html",
                                user=user,
                                playlists=playlists)

    return render_template("unauthorized.html")


def check_authorization(user_id):
    """Check to see if the logged in user is authorized to view page."""

    # Get the current user's id.
    session_user_id = session.get("user_id")

    # If correct user is not logged in, return False.
    if session_user_id != user_id:
        return False

    return True

@app.route("/play-music")
def play_music():
    """web player"""
    user_id = session.get("user_id")
    playlist_id = request.args.get('playlist_id')
    playlist = Playlist.query.get(playlist_id)

    token = session.get('access_token')

    spotify_api.play_playlist_on_web_player(user_id, playlist.playlist_title, token)

    return f'Playing playlist {playlist.playlist_title} on Spotify.'





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
